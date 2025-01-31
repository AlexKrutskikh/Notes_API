from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.animals.models import Animal
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Vetbook, VetbookFile
from .validators import validate_create_data

"""Сохранение в БД данных о веткнижке"""


class CreateVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.data

        try:
            validated_data = validate_create_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
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
            return Response(
                {"message": "Vetbook created successfully", "vetbook_id": vetbook.id}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddPhotoToVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
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
