from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User

from .models import Animal
from .validators import validate_animal_data

"""Сохранение в БД данных о животном и возврат id"""


class AddAnimalAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new animal record for the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "species": openapi.Schema(type=openapi.TYPE_STRING, description="Species of the animal"),
                "gender": openapi.Schema(type=openapi.TYPE_STRING, description="Gender of the animal"),
                "weight": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Weight of the animal"),
                "is_homeless": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is the animal homeless?"),
            },
            required=["species", "gender", "weight", "is_homeless"],  # Required fields
        ),
        responses={
            201: openapi.Response(
                description="Animal successfully created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "id_animal": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of created animal"),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request - Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )

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
                species=validate_data.get("species"),
                gender=validate_data.get("gender"),
                weight=validate_data.get("weight"),
                is_homeless=validate_data.get("is_homeless"),
            )

            return Response({"message": "Successfully created", "id_animal": animal.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
