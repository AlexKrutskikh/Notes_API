from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileViewSerializer
from apps.auth.serializers import LoginSerializer
from apps.verification_codes.serializers import SMSVerificationSerializer
from apps.verification_codes.utils import send_sms



"""Авторизация Twilio"""

class RegisterView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        photo = request.FILES.get('photo', None)

        # Проверка, переданы ли необходимые данные
        if not name or not phone:
            return Response(
                {"detail": "Необходимо указать имя и номер телефона."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка, существует ли пользователь с данным номером телефона
        if Profile.objects.filter(phone=phone).exists():
            return Response(
                {"detail": "Пользователь уже зарегистрирован. Перейдите в окно входа."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем новый профиль
        profile = Profile.objects.create(
            name=name,
            phone=phone,
            photo=photo  # Устанавливаем фото, если оно передано
        )

        # Генерируем и отправляем SMS-код
        profile.generate_sms_code()

        try:
            send_sms(profile.phone, f"Ваш код: {profile.sms_code}")
        except TwilioRestException:
            # Удаляем профиль, если SMS не может быть отправлено
            profile.delete()
            return Response(
                {"detail": "С текущими номерами отправителя и получателя SMS не может быть отправлено."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Возвращаем ответ об успешной регистрации
        return Response(
            {"detail": "Регистрация прошла успешно."},
            status=status.HTTP_201_CREATED
        )


