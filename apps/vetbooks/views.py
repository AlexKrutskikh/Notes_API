from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.animals.models import Animal
from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User
from apps.questions.models import Question
from FreeVet.utils import save_files_to_storage

from .models import (
    AppointmentFile,
    ClinicalExaminationFile,
    Vetbook,
    VetbookFile,
    Vetpass,
)
from .validators import validate_create_data

"""Сохранение в БД данных о веткнижке"""


class CreateVetbook(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
    Create a Vetbook using either an existing question or new animal data.

    **Request Body Options:**

    1. **Using an Existing Question:**
    ```json
    {
        "question_id": 1,
        "name": "Druzhok"
    }
    ```

    2. **Using New Animal Data:**
    ```json
    {
        "name": "Druzhok",
        "species": "dog",
        "gender": "male",
        "weight": 10.5,
        "is_homeless": false,
        "files_ids": [1, 2, 3]
    }
    ```

    """,
        request_body=None,  # No explicit schema, only description
        responses={
            201: openapi.Response(
                "Vetbook successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Created Vetbook ID"),
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request - Multiple Possible Errors",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Possible error messages",
                            enum=[
                                "Unable to create a vetbook due to status",
                                "InvalidQuestionId",
                                "InvalidFilesIds",
                                "InvalidName",
                                "InvalidSpecies",
                                "InvalidGender",
                                "InvalidWeight",
                                "InvalidIsHomeless" "Missing required fields",
                            ],
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        data = request.data

        # ONLY FOR TESTING PURPOSES
        user.status = "Done"

        # Only users with status "Vetbook_creation" or "Done" are allowed to create a vetbook
        if user.status not in ["Vetbook_creation", "Done"]:
            return Response({"error": "Unable to create a vetbook due to status"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if request comes from question (includes question_id and files_ids)
        is_from_question = True if data.get("question_id") else False

        # Validate data
        try:
            validated_data = validate_create_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Creating vetbook from found or newly created animal
            if is_from_question:
                question = Question.objects.select_related("animal").get(id=validated_data.get("question_id"))
                animal = question.animal
                vetbook = Vetbook.objects.create(owner=user, name=validated_data.get("name"), animal=animal)
            else:
                animal = Animal.objects.create(
                    user=user,
                    species=validated_data.get("species"),
                    gender=validated_data.get("gender"),
                    weight=validated_data.get("weight"),
                    is_homeless=validated_data.get("is_homeless"),
                )
                vetbook = Vetbook.objects.create(
                    owner=user,
                    name=validated_data.get("name"),
                    animal=animal,
                    files_ids=validated_data.get("files_ids"),
                )

            # Creating vetpass
            Vetpass.objects.create(vetbook=vetbook)

            if user.status == "Vetbook_creation":
                user.status = "Done"
                user.save()
            return Response(
                {"message": "Vetbook created successfully", "vetbook_id": vetbook.id}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Сохранение в БД файлов фотографий для веткнижки"""


class AddPhotoToVetbook(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "photos": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, format="binary"),
                    description="List of image files to upload",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                "Successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "file(s) ids": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
                        ),
                    },
                ),
            ),
            400: "Bad request - Validation error",
        },
    )
    def post(self, request):
        user_id = request.user.id

        try:

            file_paths = save_files_to_storage(request, "vetbook_photos")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        vetbook = Vetbook.objects.get(id=request.data.get("vetbook_id"))
        vetbook_files = [VetbookFile(path=path, user_id=user_id) for path in file_paths]

        VetbookFile.objects.bulk_create(vetbook_files)

        vetbook_files_instances = VetbookFile.objects.filter(path__in=file_paths)

        vetbook.vetbook_related_files.set(vetbook_files_instances)

        created_ids = list(
            VetbookFile.objects.filter(user_id=user_id).order_by("-id")[: len(file_paths)].values_list("id", flat=True)
        )

        return Response({"message": "Successfully created", "file(s) ids": created_ids}, status=201)


class GetVetbookDetails(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "vetbook_id", openapi.IN_PATH, description="ID of the Vetbook", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                "Successfully retrieved vetbook",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                        "owner_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Owner ID"),
                        "animal_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Animal ID"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Vetbook name"),
                        "photos": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of photo URLs",
                        ),
                        "treatments": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="List of treatments",
                        ),
                        "appointments": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="List of appointments",
                        ),
                    },
                ),
            ),
            400: "Bad request",
        },
    )
    def get(self, request, vetbook_id):
        vetbook = get_object_or_404(Vetbook, id=vetbook_id)
        try:
            # Get related files & photos
            photos = [
                f"{settings.MEDIA_URL}{file.path}"
                for file in vetbook.vetbook_related_files.all()
                if default_storage.exists(file.path)
            ]

            # Fetch related treatments
            treatments = list(vetbook.vetbook_treatments.values())

            # Fetch related appointments
            appointments = []
            appointments_object = vetbook.vetbook_appointments.all()

            for appointment in appointments_object:
                # Fetch all file IDs at once
                examination_files = AppointmentFile.objects.filter(id__in=appointment.examination_files_ids)
                other_files = AppointmentFile.objects.filter(id__in=appointment.other_files_ids)

                appointments.append(
                    {
                        "id": appointment.id,
                        "clinic_name": appointment.clinic_name,
                        "visit_date": appointment.visit_date,
                        "complaints": appointment.complaints,
                        "doctor_report": appointment.doctor_report,
                        "examination_files_urls": [
                            f"{settings.MEDIA_URL}{file.path}"
                            for file in examination_files
                            if default_storage.exists(file.path)
                        ],
                        "other_files_urls": [
                            f"{settings.MEDIA_URL}{file.path}"
                            for file in other_files
                            if default_storage.exists(file.path)
                        ],
                    }
                )

            # Construct Response
            response_data = {
                "id": vetbook.id,
                "owner_id": vetbook.owner.id,
                "animal_id": vetbook.animal.id,
                "name": vetbook.name,
                "created_at": vetbook.created_at,
                "updated_at": vetbook.updated_at,
                "photos": photos,
                "treatments": list(treatments),
                "appointments": appointments,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetVetpassDetails(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "vetbook_id", openapi.IN_PATH, description="ID of the Vetbook", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                "Successfully retrieved vetpass",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "additional_description": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "identification": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "vaccination_rabies": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "vaccination_others": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "deworming": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "ectoparasite_treatment": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                        "clinical_examination": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                                    "result": openapi.Schema(type=openapi.TYPE_STRING),
                                    "files": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(type=openapi.TYPE_STRING),
                                        description="List of file URLs",
                                    ),
                                },
                            ),
                        ),
                        "registration": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)
                        ),
                    },
                ),
            ),
            400: "Bad request",
        },
    )
    def get(self, request, vetbook_id):
        vetbook = get_object_or_404(Vetbook, id=vetbook_id)
        try:
            # Get Vetpass
            vetpass_object = vetbook.vetbooks_vetpass.first()
            vetpass = {
                "id": vetpass_object.id,
                "additional_description": list(vetpass_object.vetpass_additional_description.values()),
                "identification": list(vetpass_object.vetpass_identification.values()),
                "vaccination_rabies": list(vetpass_object.vetpass_vaccination_against_rabies.values()),
                "vaccination_others": list(vetpass_object.vetpass_other_vaccinations.values()),
                "deworming": list(vetpass_object.vetpass_deworming.values()),
                "ectoparasite_treatment": list(vetpass_object.vetpass_ectoparasite_treatment.values()),
                "clinical_examination": [
                    {
                        "id": examination.id,
                        "date": examination.date,
                        "result": examination.result,
                        "files": [
                            f"{settings.MEDIA_URL}{file.path}"
                            for file in examination.examination_files.all()
                            if default_storage.exists(file.path)
                        ],
                    }
                    for examination in vetpass_object.vetpass_examinations.all()
                ],
                "registration": list(vetpass_object.vetpass_registration.values()),
            }

            return Response(vetpass, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
