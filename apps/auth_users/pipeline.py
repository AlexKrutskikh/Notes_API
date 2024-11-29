from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthException
from datetime import datetime


def generate_jwt(user):

    if user is None:
        raise AuthException("User does not exist or was not found.")  # Выбросить исключение, если user равен None

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return {
        'access': str(access_token),
        'refresh': str(refresh)
    }


def create_user(strategy, details, backend, user=None, *args, **kwargs):

    email = kwargs.get('email', details.get('email'))

    User = get_user_model()
    existing_user = User.objects.filter(email=email).first()

    if existing_user:
        existing_user.last_login = datetime.now()
        existing_user.save()

        jwt_tokens = generate_jwt(existing_user)

        response = strategy.redirect('https://127.0.0.1:8000/api/auth_users/updatecode/')
        response.set_cookie('jwt_access_token', jwt_tokens['access'], httponly=True, secure=True)
        response.set_cookie('jwt_refresh_token', jwt_tokens['refresh'], httponly=True, secure=True)

        return response

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

    jwt_tokens = generate_jwt(user)

    strategy.session_set('jwt_access_token', jwt_tokens['access'])
    strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

    strategy.redirect('https://freevet.me/verification/role')

