import random

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.specialist_info.models import Specialist

from .models import VerificationCode


class GenerateVerificationCode(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only admin can generate verification codes"}, status=status.HTTP_403_FORBIDDEN)

        code = str(random.randint(100000, 999999))  # Генерация кода
        VerificationCode.objects.create(code=code)  # Код просто сохраняется в базе

        return Response({"message": "Verification code generated", "code": code}, status=status.HTTP_201_CREATED)


class VerifySpecialist(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        specialist_id = request.data.get("specialist_id")
        code = request.data.get("code")

        try:
            specialist = Specialist.objects.get(id=specialist_id)
        except Specialist.DoesNotExist:
            return Response({"error": "Specialist not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            verification_code = VerificationCode.objects.get(code=code, is_used=False)

            # Обновляем статус верификации специалиста
            specialist.is_verified = True
            specialist.save()

            # Отмечаем код как использованный
            verification_code.is_used = True
            verification_code.save()

            return Response({"message": "Specialist verified successfully"}, status=status.HTTP_200_OK)
        except VerificationCode.DoesNotExist:
            return Response({"error": "Invalid or used verification code"}, status=status.HTTP_400_BAD_REQUEST)
