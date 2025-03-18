from django.urls import include, path

from .auth_view import AuthorizationUser, RegistrationUser
from .authentication import CustomTokenRefreshView
from .social_view import google_oauth_redirect

urlpatterns = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    # api бибsqlite_sequenceлиотеки social-auth-app-django
    path("social-auth/", include("social_django.urls", namespace="social")),
    # регистрация и авторизация google
    path("v1/authentication/google/", google_oauth_redirect, name="google-login-shortcut"),
    # регистрация
    path("v1/registration/user/", RegistrationUser.as_view(), name="RegistrationUser"),
    # вход
    path("v1/authorization/user/", AuthorizationUser.as_view(), name="AuthorizationUser"),
]
