from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.auth.models import SmsCode
from apps.auth.serializers import SendSmsCodeSerializer
from twilio.base.exceptions import TwilioRestException
import secrets
from django.utils import timezone
from .utils import send_sms

"""Функция для получения IP-адреса из запроса"""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


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
        sent_time = timezone.now()

        try:
            send_sms(phone, f"Ваш код: {code}")
        except TwilioRestException:
            return Response(
                {

                    "error_type": "WrongPhone",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        ip = get_client_ip(request)

        SmsCode.objects.create(
            phone=phone,
                code=code,
                sent_time=sent_time,
                ip=ip
        )


        return Response(

            {

                "type": "Successful operation"

            },
            status=status.HTTP_201_CREATED
        )

