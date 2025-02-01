from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.auth.models import User

from .models import Specialist, SpecialistDocument
from .validators import validate_specialist_data

"""Сохранение в БД данных о животном и возврат id"""


class AddSpecialist(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.data
        documents = request.FILES.getlist("documents")

        # Проверка на наличие хотя бы одного документа
        if not documents:
            return Response({"error": "At least one document is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_data = validate_specialist_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # Проверка, существует ли уже специалист для пользователя
        if Specialist.objects.filter(user=user).exists():
            return Response({"error": "User is already a specialist"}, status=status.HTTP_400_BAD_REQUEST)

        specialist = Specialist.objects.create(
            user=user,
            name=validated_data.get("name"),
            last_name=validated_data.get("last_name"),
            specialization=validated_data.get("specialization"),
            animals=validated_data.get("animals"),
            additional_info=validated_data.get("additional_info", ""),
            telegram=validated_data.get("telegram"),
        )

        # Сохранение документов
        for doc in documents:
            if doc:
                SpecialistDocument.objects.create(document=doc, specialist=specialist)

        return Response(
            {
                "message": "Specialist created successfully",
                "specialist_id": specialist.id,
                "user_id": specialist.user.id,
            },
            status=status.HTTP_201_CREATED,
        )
