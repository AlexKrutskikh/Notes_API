from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.auth.models import SmsCode, User
from apps.auth.serializers import SendSmsCodeSerializer
from twilio.base.exceptions import TwilioRestException
import secrets
from django.utils import timezone
from .utils import send_sms
from django.conf import settings
from .utils import generate_token_and_redirect, get_client_ip


"""Генерация и отправки SMS-кода"""

class SendSmsCode(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        existing_entry = SmsCode.objects.filter(phone=phone).last()

        if existing_entry and existing_entry.sent_time:
            time_since_sent = timezone.now() - existing_entry.sent_time

            if time_since_sent < timedelta(seconds=60):
                return Response(
                    {

                        "error_type": "remainingSeconds",

                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        code = ''.join(secrets.choice("0123456789") for _ in range(6))


        if settings.SEND_SMS:
            try:
                send_sms(phone, f"Ваш код: {code}")
            except TwilioRestException:
                return Response(
                    {

                        "error_type": "WrongPhone",

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


        SmsCode.objects.create(
            phone = phone,
                code = code,
                sent_time = timezone.now(),
                ip = get_client_ip(request)
        )

        return Response(

            {

                "type": "Successful operation"

            },
            status=status.HTTP_201_CREATED
        )

"""Проверка смс-кода и верификации пользователя по телефону"""

class VerifySmsCode(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        existing_entry = SmsCode.objects.filter(phone=phone).last()

        if not existing_entry:
            return Response(
                {"error_type": "PhoneNotFound"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if existing_entry.sent_time and (timezone.now() - existing_entry.sent_time) > timedelta(minutes=5):
            return Response(
                {"error_type": "CodeExpired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if existing_entry.code != code:
            return Response(
                {"error_type": "InvalidCode"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_exist = User.objects.filter(phone=phone).first()


        if  user_exist:
            user_exist.last_login = timezone.now()
            user_exist.save()

            return generate_token_and_redirect(user_exist, redirect_url=f"{settings.BASE_URL}/main/")

        else:

            user = User.objects.create(
                phone=phone,
                registration_time= timezone.now()
            )


            return generate_token_and_redirect(user, redirect_url=f"{settings.BASE_URL}/verification/role/")






