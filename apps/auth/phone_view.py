import secrets
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from apps.auth.models import SmsCode, User
from .utils import generate_token_set_cookie, get_client_ip, send_sms
from .validators import validate_phone_code

"""Генерация и отправки SMS-кода"""


class SendSmsCode(APIView):

    def post(self, request, *args, **kwargs):

        try:
          validate_data = validate_phone_code(data=request.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        phone = validate_data.get("phone")

        existing_entry = SmsCode.objects.filter(phone=phone).last()

        if existing_entry and existing_entry.sent_time:
            time_since_sent = timezone.now() - existing_entry.sent_time

            if time_since_sent < timedelta(seconds=60):
                return Response(
                    {
                        "error": "remainingSeconds",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        code = "".join(secrets.choice("0123456789") for _ in range(6))

        if settings.SEND_SMS:
            try:
                send_sms(phone, f"Ваш код: {code}")
            except TwilioRestException:
                return Response(
                    {
                        "error": "WrongPhone",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        SmsCode.objects.create(phone=phone, code=code, sent_time=timezone.now(), ip=get_client_ip(request))

        return Response({"type": "Successful operation"}, status=status.HTTP_201_CREATED)


"""Проверка смс-кода и верификации пользователя по телефону"""


class VerifySmsCode(APIView):

    def post(self, request, *args, **kwargs):

        try:
            validate_data = validate_phone_code(data=request.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        phone = validate_data.get("phone")
        code = validate_data.get("code")

        existing_entry = SmsCode.objects.filter(phone=phone).last()

        if not existing_entry:
            return Response({"error": "PhoneNotFound"}, status=status.HTTP_400_BAD_REQUEST)

        if existing_entry.sent_time and (timezone.now() - existing_entry.sent_time) > timedelta(minutes=5):
            return Response({"error": "CodeExpired"}, status=status.HTTP_400_BAD_REQUEST)

        if existing_entry.code != code:
            return Response({"error": "InvalidCode"}, status=status.HTTP_400_BAD_REQUEST)

        user_exist = User.objects.filter(phone=phone).first()

        if user_exist:
            user_exist.last_login = timezone.now()
            user_exist.save()

        else:

            user = User.objects.create(phone=phone, registration_time=timezone.now())

            response = Response({"type": "Successful operation"}, status=status.HTTP_201_CREATED)

            generate_token_set_cookie(user, response)


        return response
