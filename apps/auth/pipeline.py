from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from social_core.exceptions import AuthException

from apps.profiles.models import Profile
from FreeVet import settings

from .utils import generate_token_and_redirect

""" Создаёт или обновляет пользователя на основе данных, полученных от провайдера социальной аутентификации.
    Генерирует JWT-токены для пользователя и перенаправляет его на указанный URL"""


def create_user(strategy, details, backend, user=None, *args, **kwargs):

    email = kwargs.get("email", details.get("email"))

    User = get_user_model()
    user = User.objects.filter(email=email).first()

    if user:
        user.last_login = datetime.now()
        user.save()

    else:

        uid = kwargs.get("uid") or kwargs.get("response", {}).get("sub")
        if not uid:
            raise AuthException("UID is missing.")

        provider = backend.name

        if provider == "google-oauth2":

            username = kwargs.get("username", email.split("@")[0])
            first_name = kwargs.get("response", {}).get("given_name", "")
            last_name = kwargs.get("response", {}).get("family_name", "")

            fields = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "auth_provider": provider,
            }

            user = User(**fields)
            user.save()

            Profile.objects.create(
                user=user, name=first_name, last_name=last_name, email=email, created_at=timezone.now()
            )

        elif provider == "facebook":

            username = kwargs.get("username", email.split("@")[0])
            first_name = kwargs.get("response", {}).get("name", "").split(" ")[0]
            last_name = kwargs.get("response", {}).get("name", "").rsplit(" ")[1]

            fields = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "auth_provider": provider,
            }

            user = User(**fields)
            user.save()

            Profile.objects.create(
                user=user, name=first_name, last_name=last_name, email=email, created_at=timezone.now()
            )

    return generate_token_and_redirect(user, redirect_url=f"{settings.BASE_URL}/main/")
