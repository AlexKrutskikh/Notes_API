from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import AuthException

from .redis_token import add_token_to_whitelist

"""Генерирует JWT-токены, устанавливает их в cookies и перенаправляет на заданный URL"""


def generate_token_and_set_cookie(user, request):

    if user is None:
        raise AuthException("User does not exist or was not found.")

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    jwt_tokens = {"access": str(access_token), "refresh": str(refresh)}

    response = Response({"access_token": str(access_token), "refresh_token": str(refresh)})

    ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    add_token_to_whitelist(jwt_tokens["access"], user.id, 7, ip, user_agent)

    response.set_cookie("access_token", jwt_tokens["access"], httponly=True, secure=True, samesite="None")
    response.set_cookie("refresh_token", jwt_tokens["refresh"], httponly=True, secure=True, samesite="None")

    return response


"""Получение IP-адреса из запроса"""


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip
