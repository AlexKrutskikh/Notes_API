from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthException
from datetime import datetime
from FreeVet import settings


def generate_token_and_redirect(strategy, user, redirect_url):

    """
    Генерирует JWT-токены, устанавливает их в cookies и перенаправляет на заданный URL.

    :param user: Объект пользователя, для которого нужно сгенерировать токены.
    :param redirect_url: URL для переадресации.
    :return: HttpResponseRedirect с установленными cookies.
    """

    if user is None:
        raise AuthException("User does not exist or was not found.")

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    jwt_tokens = {
        'access': str(access_token),
        'refresh': str(refresh)
    }

    response = strategy.redirect(redirect_url)

    response.set_cookie('jwt_access_token', jwt_tokens['access'], httponly=True, secure=True,samesite=None)
    response.set_cookie('jwt_refresh_token', jwt_tokens['refresh'], httponly=True, secure=True,samesite=None)
    response = strategy.redirect(redirect_url)

    return response

""" Создаёт или обновляет пользователя на основе данных, полученных от провайдера социальной аутентификации.
    Генерирует JWT-токены для пользователя и перенаправляет его на указанный URL"""


def create_user(strategy, details, backend, user=None, *args, **kwargs):

    email = kwargs.get('email', details.get('email'))

    User = get_user_model()
    existing_user = User.objects.filter(email=email).first()

    if existing_user:
        existing_user.last_login = datetime.now()
        existing_user.save()

        return generate_token_and_redirect(existing_user, redirect_url = f"{settings.BASE_URL}/main/")


    uid = kwargs.get('uid') or kwargs.get('response', {}).get('sub')
    if not uid:
        raise AuthException("UID is missing.")

    username = kwargs.get('username', email.split('@')[0])
    first_name = kwargs.get('response', {}).get('given_name', '')
    last_name = kwargs.get('response', {}).get('family_name', '')

    fields = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'auth_provider': backend.name
    }

    user = User(**fields)
    user.save()

    return generate_token_and_redirect(user, redirect_url=f"{settings.BASE_URL}/verification/role/")

