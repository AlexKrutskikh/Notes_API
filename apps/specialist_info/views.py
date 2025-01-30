from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.models import User

from .models import Specialist


class SpecialistCreateAPIView(APIView):

    def post(self, request):
        user_id = request.data.get("user_id")
        name = request.data.get("name")
        last_name = request.data.get("last_name")
        document = request.FILES.get("document")
        specialization = request.data.get("specialization")
        animals = request.data.get("animals")
        additional_info = request.data.get("additional_info", "")

        # Проверяем, существует ли пользователь
        user = get_object_or_404(User, id=user_id)

        # Проверяем, не является ли он уже специалистом
        if Specialist.objects.filter(user=user).exists():
            return Response({"error": "User is already a specialist"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаём специалиста
        specialist = Specialist.objects.create(
            user=user,
            name=name,
            last_name=last_name,
            document=document,
            specialization=specialization,
            animals=animals,
            additional_info=additional_info,
        )

        return Response(
            {
                "message": "Specialist created successfully",
                "specialist_id": specialist.id,
                "user_id": specialist.user.id,
            },
            status=status.HTTP_201_CREATED,
        )
