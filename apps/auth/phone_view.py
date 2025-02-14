import secrets
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException

from apps.auth.models import SmsCode, User
from apps.profiles.models import Profile

from .utils import generate_token_and_redirect, get_client_ip, send_sms
from .validators import validate_phone_code

"""Генерация и отправки SMS-кода"""


class SendSmsCode(APIView):

    @swagger_auto_schema(
        operation_description="Send an SMS code for phone verification.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number in international format."),
            },
            required=["phone"],
        ),
        responses={
            201: openapi.Response(
                "SMS code sent successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "type": openapi.Schema(type=openapi.TYPE_STRING, description="Operation result"),
                        "code": openapi.Schema(type=openapi.TYPE_STRING, description="Generated SMS verification code"),
                    },
                ),
            ),
            400: openapi.Response("Bad Request - Validation Error or Rate Limit Exceeded"),
            500: openapi.Response("Server Error - SMS Sending Failed"),
        },
    )
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

        code = SmsCode.objects.create(phone=phone, code=code, sent_time=timezone.now(), ip=get_client_ip(request))

        return Response({"type": "Successful operation", "code": code.code}, status=status.HTTP_201_CREATED)


"""Проверка смс-кода и верификации пользователя по телефону"""


class VerifySmsCode(APIView):

    @swagger_auto_schema(
        operation_description="Verify the SMS code for user authentication.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number used to receive the SMS."),
                "code": openapi.Schema(type=openapi.TYPE_STRING, description="The 6-digit code received via SMS."),
            },
            required=["phone", "code"],
        ),
        responses={
            200: openapi.Response(
                "Verification successful",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Verification success message"),
                        "redirect_url": openapi.Schema(
                            type=openapi.TYPE_STRING, description="URL to redirect the user"
                        ),
                    },
                ),
            ),
            400: openapi.Response("Bad Request - Invalid Code or Expired Code"),
        },
    )
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

        user = User.objects.filter(phone=phone).first()

        if user:
            user.last_login = timezone.now()
            user.save()

        else:

            user = User.objects.create(phone=phone, registration_time=timezone.now())
            Profile.objects.create(user=user, phone=phone, created_at=timezone.now())

        return generate_token_and_redirect(user, redirect_url=f"{settings.BASE_URL}/main/")
