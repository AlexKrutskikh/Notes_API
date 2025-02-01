from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

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


class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token not found in cookies"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            refresh = RefreshToken(refresh_token)

            access_token = str(refresh.access_token)

            new_refresh_token = str(refresh)

            response = Response({"access": access_token, "refresh": new_refresh_token}, status=status.HTTP_200_OK)
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", new_refresh_token, httponly=True, secure=True, samesite="Lax")

            return response

        except (InvalidToken, TokenError) as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
