from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    custom_login_redirect,
    google_oauth_redirect,
    facebook_oauth_redirect, ProfileView
)
from .views import RegisterView, LoginView, VerifyCodeView, UpdateProfileFieldsView, UpdateVerifyCodeView, VerifyCodeVetView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('social-auth/',
         include('social_django.urls', namespace='social')), #social-auth

    path('redirect/', custom_login_redirect, name='custom_login_redirect'), #Redirect after registration and authorization

    path('login/google/', google_oauth_redirect, name='google-login-shortcut'), #Short API for authorization google

    path('login/facebook/', facebook_oauth_redirect, name='facebook-login-shortcut'), #Short API for authorization facebook

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
 
    path('update_verify_code/',UpdateVerifyCodeView.as_view(), name='Update_VerifyCode'),

    path('verify_code_vet/', VerifyCodeVetView.as_view(), name='verify_code_vet'),

    path('profile/<pk>', ProfileView.as_view(), name='profile'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
