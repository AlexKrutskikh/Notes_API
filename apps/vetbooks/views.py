from django.core.exceptions import ValidationError
from django.utils.timezone import now
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
    AdditionalDescription,
    ClinicalExamination,
    Deworming,
    EctoparasiteTreatment,
    Identification,
    Registration,
    VaccinationAgainstRabies,
    VaccinationOthers,
    Vetbook,
    VetbookFile,
    Vetpass,
)
from .validators import (
    validate_additional_description,
    validate_create_data,
    validate_identification,
)

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
            400: "Bad Request - Validation Error",
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
            return Response({"error": "Unable to create a vetbook"}, status=status.HTTP_400_BAD_REQUEST)

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
                    name=validated_data.get("name"),
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

            # Creating vetpass and its blank instances
            vetpass = Vetpass.objects.create(vetbook=vetbook)
            AdditionalDescription.objects.create(vetpass=vetpass)
            Identification.objects.create(vetpass=vetpass)
            VaccinationAgainstRabies.objects.create(vetpass=vetpass)
            VaccinationOthers.objects.create(vetpass=vetpass)
            Deworming.objects.create(vetpass=vetpass)
            EctoparasiteTreatment.objects.create(vetpass=vetpass)
            ClinicalExamination.objects.create(vetpass=vetpass)
            Registration.objects.create(vetpass=vetpass)

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

        vetbook_files = [VetbookFile(path=path, user_id=user_id) for path in file_paths]

        created_objects = VetbookFile.objects.bulk_create(vetbook_files)

        created_ids = [obj.id for obj in created_objects]

        return Response({"message": "Successfully created", "file(s) ids": created_ids}, status=201)


""" Переиспользуемая функция для получения веткнижки и ветпаспорта """


def get_vetbook_and_vetpass(request, validated_data):
    """Retrieve the vetbook and vetpass, ensuring the user is authorized."""
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        vetbook = Vetbook.objects.get(id=validated_data["vetbook_id"])
    except User.DoesNotExist:
        return None, None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Vetbook.DoesNotExist:
        return None, None, Response({"error": "Vetbook not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the owner of the vetbook
    if user != vetbook.owner:
        return None, None, Response({"error": "Not authorized to edit the vetbook"}, status=status.HTTP_403_FORBIDDEN)

    try:
        vetpass = Vetpass.objects.get(vetbook=vetbook)
    except Vetpass.DoesNotExist:
        return None, None, Response({"error": "Vetpass not found for this vetbook"}, status=status.HTTP_404_NOT_FOUND)

    return vetbook, vetpass, None


""" Изменение дополнительного описания в ветпаспорте """


class EditAdditionalDescription(APIView):
    def patch(self, request):
        # Validate data
        data = request.data
        try:
            validated_data = validate_additional_description(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response

        # Get or create AdditionalDescription
        additional_info = AdditionalDescription.objects.get(vetpass=vetpass)

        # Update fields if present in the request
        for field in ["breed", "color", "birth_date", "special_marks"]:
            if field in validated_data:
                setattr(additional_info, field, validated_data[field])

        additional_info.save()

        # Update vetbook's updated_at field
        vetbook.updated_at = now()
        vetbook.save()

        return Response(
            {"message": "Additional information updated successfully"},
            status=status.HTTP_200_OK,
        )


class EditIdentification(APIView):
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_identification(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found

        # Get or create Identification
        identification = Identification.objects.get(vetpass=vetpass)

        # Update fields if present in the request
        for field in ["chip_number", "clinic", "chip_installation_location", "date"]:
            if field in validated_data:
                setattr(identification, field, validated_data[field])

        identification.save()

        # Update vetbook's updated_at field
        vetbook.updated_at = now()
        vetbook.save()

        return Response({"message": "Identification information updated successfully"}, status=status.HTTP_200_OK)
