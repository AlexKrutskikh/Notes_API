from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from social_core.exceptions import AuthException


# Функция для генерации JWT токенов
def generate_jwt(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return {
        'access': str(access_token),
        'refresh': str(refresh)
    }

# Ваш кастомный пайплайн для создания пользователя
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    print("Data received from social login:", kwargs)

    # Если пользователь существует, генерируем JWT токены
    if user:
        jwt_tokens = generate_jwt(user)
        strategy.session_set('jwt_access_token', jwt_tokens['access'])
        strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])
        return HttpResponseRedirect('https://freevet.me/verification/role')

    # Если пользователь новый, создаем его
    uid = kwargs.get('uid') or kwargs.get('response', {}).get('sub')
    if not uid:
        raise AuthException("UID is missing.")  # Это поможет избежать ошибки, если uid не передан

    # Используем email или создаем username на основе имени
    email = kwargs.get('email', details.get('email'))
    username = kwargs.get('username', email.split('@')[0])  # Можно использовать email до символа "@" как username

    # Заполнение данных для нового пользователя
    fields = {
        'username': username,
        'email': email,
        'first_name': kwargs.get('given_name', details.get('given_name', '')),
        'last_name': kwargs.get('family_name', details.get('family_name', '')),
        # Добавьте остальные поля, которые должны быть сохранены
    }

    # Проверяем, существует ли пользователь с таким email
    User = get_user_model()
    if User.objects.filter(email=email).exists():
        raise AuthException("User with this email already exists.")

    # Создание нового пользователя
    user = strategy.create_user(**fields)
    jwt_tokens = generate_jwt(user)

    # Сохраняем JWT токены в сессии
    strategy.session_set('jwt_access_token', jwt_tokens['access'])
    strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

    # Редирект на страницу после успешного создания пользователя
    return HttpResponseRedirect('https://freevet.me/main/')
