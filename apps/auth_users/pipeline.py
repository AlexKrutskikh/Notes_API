from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.shortcuts import redirect



def round_to_minute(dt):
    return dt.replace(second=0, microsecond=0)


def redirect_after_login(backend, user, response, *args, **kwargs):

    registration_time_rounded = round_to_minute(user.registration_time)
    last_login_time_rounded = round_to_minute(user.last_login_time)

    if registration_time_rounded == last_login_time_rounded:
        redirect_url = f'https://freevet.me/verification/role'

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
    else:
        redirect_url = 'https://freevet.me/main'
        access_token = None
        refresh_token = None

    request = kwargs.get('request')

    if request:
        if access_token and refresh_token:
            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': redirect_url
            }
            return JsonResponse(response_data)

        request.session['redirect_url'] = redirect_url
        return redirect(redirect_url)

    return user


def set_auth_provider(backend, user, *args, **kwargs):
    if user:
        user.auth_provider = backend.name  # 'google-oauth2', 'facebook', и т.д.
        user.save()
