from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.auth.models import SmsCode
from apps.auth.serializers import SendSmsCodeSerializer
from twilio.base.exceptions import TwilioRestException
import random
from django.utils import timezone
from .utils import send_sms


"""Эндпоинт для генерации и отправки SMS-кода"""

class SendSmsCode(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        existing_entry = SmsCode.objects.filter(phone=phone).first()

        if existing_entry and existing_entry.sms_code:
            time_since_sent = timezone.now() - existing_entry.code_sent_time
            if time_since_sent.total_seconds() < 300:  # 5 минут
                return Response(
                    {
                        "error_type": "CodeAlreadySent",
                        "detail": "Код уже отправлен. Пожалуйста, подождите."
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
                    "error_type": "SmsSendError",
                    "detail": "Ошибка отправки SMS."
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
            {"detail": "SMS-код успешно отправлен."},
            status=status.HTTP_201_CREATED
        )

