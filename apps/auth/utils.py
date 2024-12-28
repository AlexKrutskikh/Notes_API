from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import AuthException
from twilio.rest import Client


"""Отправка SMS Twilio"""


def send_sms(phone, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Your verification code is: {verification_code}", from_=settings.TWILIO_NUMBER, to=str(phone)
    )

    return message.sid


"""Генерирует JWT-токены"""


def generate_token_set_cookie(user,response):

    if user is None:
        raise AuthException("User does not exist or was not found.")

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    jwt_tokens = {"access": str(access_token), "refresh": str(refresh)}
    print(1111111111111111)

    response.set_cookie("access_token", jwt_tokens["access"], httponly=True, secure=True, samesite=None)
    response.set_cookie("refresh_token", jwt_tokens["refresh"], httponly=True, secure=True, samesite=None)

    return response


"""Получение IP-адреса из запроса"""

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip
