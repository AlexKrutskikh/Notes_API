from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return None

        try:
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token["user_id"])
        except Exception:
            raise AuthenticationFailed("InvalidToken")

        return (user, None)
