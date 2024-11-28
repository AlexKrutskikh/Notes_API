from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from social_core.exceptions import AuthException


# Функция для генерации JWT токенов
def generate_jwt(user):
    # Проверяем, существует ли пользователь перед генерацией токенов
    if user is None:
        raise AuthException("User does not exist or was not found.")  # Выбросить исключение, если user равен None

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return {
        'access': str(access_token),
        'refresh': str(refresh)
    }

# Ваш кастомный пайплайн для создания пользователя
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    print("kwargs:", kwargs)  # Печать всего содержимого kwargs
    # Получаем email пользователя
    email = kwargs.get('email', details.get('email'))

    # Проверка, существует ли пользователь с таким email
    User = get_user_model()
    existing_user = User.objects.filter(email=email).first()

    # Если пользователь существует, обновляем его last_login и сохраняем токены
    if existing_user:
        existing_user.last_login = existing_user.date_joined
        existing_user.save()

        jwt_tokens = generate_jwt(existing_user)

        strategy.session_set('jwt_access_token', jwt_tokens['access'])
        strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

        return HttpResponseRedirect('https://freevet.me/main/')

    # Если пользователя нет, создаем нового
    uid = kwargs.get('uid') or kwargs.get('response', {}).get('sub')
    if not uid:
        raise AuthException("UID is missing.")

    username = kwargs.get('username', email.split('@')[0])

    # Извлекаем first_name и last_name из response
    first_name = kwargs.get('response', {}).get('given_name', '')
    last_name = kwargs.get('response', {}).get('family_name', '')

    print("kwargs:", kwargs)  # Печать всего содержимого kwargs

    # Заполнение данных для нового пользователя
    fields = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }

    # Создание нового пользователя без пароля
    user = User(**fields)
    user.set_unusable_password()  # Устанавливаем недействительный пароль
    user.save()

    jwt_tokens = generate_jwt(user)

    strategy.session_set('jwt_access_token', jwt_tokens['access'])
    strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

    return HttpResponseRedirect('https://freevet.me/verification/role')

