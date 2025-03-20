from django.urls import include, path

from .auth_view import AuthorizationUser, LogoutView, RegistrationUser
from .authentication import CustomTokenRefreshView

urlpatterns = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    # регистрация
    path("v1/registration/user/", RegistrationUser.as_view(), name="RegistrationUser"),
    # вход
    path("v1/authorization/user/", AuthorizationUser.as_view(), name="AuthorizationUser"),
    # выход
    path("v1/logout/user", LogoutView.as_view(), name="logout"),
]
