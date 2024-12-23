from datetime import timedelta, timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import Profile

"""Update verify code for veterinarian"""


class UpdateVerifyCodeView(APIView):
    def post(self, request):
        # Получаем данные из запроса
        phone = request.data.get("phone")
        email = request.data.get("email")
        verify_code = request.data.get("verify_code")

        # Проверка наличия телефона или почты
        if not phone and not email:
            return Response({"error": "Either phone or email must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем профиль по телефону или email
        profile = Profile.objects.filter(phone=phone).first() or Profile.objects.filter(email=email).first()

        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем только поле verify_code
        profile.verify_code = verify_code
        profile.save()

        return Response({"message": "Verify code updated successfully."}, status=status.HTTP_200_OK)


class VerifyCodeVetView(APIView):
    def post(self, request):
        # Получаем данные из запроса
        phone = request.data.get("phone")
        email = request.data.get("email")
        input_code = request.data.get("verify_code")

        # Проверка наличия телефона или email и кода
        if not (phone or email) or not input_code:
            return Response(
                {"error": "Phone or email and verify code are required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Ищем профиль по телефону или email
        profile = Profile.objects.filter(phone=phone).first() or Profile.objects.filter(email=email).first()

        # Проверка, что профиль найден
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Проверка срока действия кода
        if profile.code_sent_time < timezone.now() - timedelta(days=5):
            return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Сравнение введенного кода с сохраненным в базе данных
        if profile.verify_code == input_code:
            return Response({"message": "Verify code is correct."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verify code."}, status=status.HTTP_400_BAD_REQUEST)
