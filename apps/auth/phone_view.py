from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.auth.models import SmsCode
from apps.auth.serializers import SendSmsCodeSerializer
from twilio.base.exceptions import TwilioRestException
import random
from django.utils import timezone
from .utils import send_sms


"""Генерация и отправки SMS-кода"""

class SendSmsCode(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        existing_entry = SmsCode.objects.filter(phone=phone).first()

        if existing_entry and existing_entry.sms_code:

            time_since_sent = timezone.now() - existing_entry.code_sent_time
            remaining_time = 300 - time_since_sent.total_seconds()

            if remaining_time > 0:
                remaining_minutes = max(1, int(remaining_time // 60) + (remaining_time % 60 > 0))

                return Response(
                    {
                        "error_type": "CodeAlreadySent",
                        "detail": f"Вы можете запросить новый код через {remaining_minutes} минут(ы)."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        sms_code = str(random.randint(100000, 999999))
        code_sent_time = timezone.now()

        try:
            send_sms(phone, f"Ваш код: {sms_code}")
        except TwilioRestException:
            return Response(
                {
                    "error_type": "WrongPhone",
                    "detail": "Неверный формат номера телефона"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


        SmsCode.objects.update_or_create(
            phone=phone,
            defaults={
                "sms_code": sms_code,
                "code_sent_time": code_sent_time
            }
        )

        return Response(

            {  "type": "Successful operation",
               "detail": "SMS-код успешно отправлен."},
            status=status.HTTP_201_CREATED
        )

