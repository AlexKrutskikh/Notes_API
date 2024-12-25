from django.conf import settings
from django.http import HttpResponseRedirect

"""API для авторизации и регистрации через социальные сети"""


def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/auth/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)


def facebook_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/auth/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)
