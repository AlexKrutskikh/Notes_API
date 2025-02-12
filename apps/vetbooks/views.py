from django.core.exceptions import ValidationError
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
from .validators import validate_create_data

"""Сохранение в БД данных о веткнижке"""


class CreateVetbook(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class AddPhotoToVetbook(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

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
