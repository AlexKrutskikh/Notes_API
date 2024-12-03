from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .phone_view import ProfileView
from .social_view import    google_oauth_redirect, facebook_oauth_redirect
from .phone_view import RegisterView, LoginView, VerifyCodeView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('social-auth/',
         include('social_django.urls', namespace='social')),                                      # api бибsqlite_sequenceлиотеки social-auth-app-django

    path('v1/authentication/google/', google_oauth_redirect, name='google-login-shortcut'),       # регистрация и авторизация google

    path('v1/authentication/facebook/', facebook_oauth_redirect, name='facebook-login-shortcut'), # регистрация и авторизация facebook














    path('register/', RegisterView.as_view(), name='register'),


    path('login/', LoginView.as_view(), name='login'),

    path('verify/', VerifyCodeView.as_view(), name='verify_code'),

    path('profile/<pk>', ProfileView.as_view(), name='profile'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
