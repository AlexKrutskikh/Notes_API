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
    print("Data received from social login:", kwargs)

    # Получаем email пользователя
    email = kwargs.get('email', details.get('email'))

    # Проверка, существует ли пользователь с таким email
    User = get_user_model()
    existing_user = User.objects.filter(email=email).first()

    # Если пользователь существует, обновляем его last_login и сохраняем токены
    if existing_user:
        # Обновляем поле last_login на дату регистрации пользователя
        existing_user.last_login = existing_user.date_joined
        existing_user.save()

        # Генерация JWT токенов
        jwt_tokens = generate_jwt(existing_user)

        # Сохраняем токены в сессии
        strategy.session_set('jwt_access_token', jwt_tokens['access'])
        strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

        # Редиректим на нужную страницу в зависимости от того, новый ли пользователь
        return HttpResponseRedirect('https://freevet.me/main/')

    # Если пользователя нет, создаем нового
    uid = kwargs.get('uid') or kwargs.get('response', {}).get('sub')
    if not uid:
        raise AuthException("UID is missing.")  # Это поможет избежать ошибки, если uid не передан

    username = kwargs.get('username', email.split('@')[0])  # Используем email как username

    # Заполнение данных для нового пользователя
    fields = {
        'username': username,
        'email': email,
        'first_name': kwargs.get('given_name', details.get('given_name', '')),
        'last_name': kwargs.get('family_name', details.get('family_name', '')),
    }

    # Создание нового пользователя
    user = strategy.create_user(**fields)

    # Генерация JWT токенов для нового пользователя
    jwt_tokens = generate_jwt(user)

    # Сохраняем JWT токены в сессии
    strategy.session_set('jwt_access_token', jwt_tokens['access'])
    strategy.session_set('jwt_refresh_token', jwt_tokens['refresh'])

    # Редирект на страницу после успешного создания пользователя
    return HttpResponseRedirect('https://freevet.me/verification/role')
