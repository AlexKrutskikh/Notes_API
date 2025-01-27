from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.auth.models import User

from .models import Animal
from .validators import validate_animal_data

"""Сохранение в БД данных о животном и возврат id"""


class AddAnimalAPIView(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data = request.data

        try:
            validate_data = validate_animal_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:

            animal = Animal.objects.create(
                user=User.objects.get(id=user_id),
                name=validate_data.get("name"),
                species=validate_data.get("species"),
                gender=validate_data.get("gender"),
                weight=validate_data.get("weight"),
                is_homeless=validate_data.get("is_homeless"),
            )

            return Response({"message": "Successfully created", "id_animal": animal.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
