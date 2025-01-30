from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.animals.models import Animal
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Vetbook
from .validators import validate_create_data

"""Сохранение в БД данных о веткнижке"""


class CreateVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.data

        try:
            photos_paths = save_files_to_storage(request, "vetbook_photos")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_data = validate_create_data(data)
            print(validated_data.get("is_homeless"))
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            animal = Animal.objects.create(
                user=user,
                gender=validated_data.get("gender"),
                weight=validated_data.weight,
                is_homeless=validated_data.is_homeless,
            )
            vetbook = Vetbook.objects.create(
                owner=user, name=validated_data.get("name"), animal=animal, photos_paths=photos_paths
            )
            print("Vetbook created successfully")

            return Response(
                {"message": "Vetbook created successfully", "vetbook_id": vetbook.id}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)