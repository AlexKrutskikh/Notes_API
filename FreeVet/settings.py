"""
Django settings for FreeVet project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from django.urls import reverse_lazy
import os
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
Env.read_env(BASE_DIR / '.env')

BASE_URL = 'https://localhost:8000'  # Base URL

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173"  # Разрешаем запросы с вашего клиентского домена
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS='127.0.0.1','localhost', '213.171.27.47'

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    'social_django',  # django-social-auth
    'drf_yasg',

    'rest_framework',
    'rest_framework.authtoken',  # Token Authentication
    'modeltranslation',

    'users',
    'vetbook',
    'questions',
    'apps',
]

"""social-auth"""

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = reverse_lazy('custom_login_redirect')  # REDIRECT after registration
SOCIAL_AUTH_URL_NAMESPACE = 'social'  # namespace social

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1039945308403-lvqi1omlavlk27qltmjtooki4hoengsd.apps.googleusercontent.com' # Google client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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' # Google client secret

SOCIAL_AUTH_FACEBOOK_KEY='1186656015942216' #Facebook client ID
SOCIAL_AUTH_FACEBOOK_SECRET='ad7c199b22dafe5e225bbe39af363b21' #Facebook client secret

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'users.pipeline.save_profile',  # Custom pipeline for creating a profile
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
)

"""End social-auth"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FreeVet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FreeVet.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Используем SQLite
            'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных (по умолчанию db.sqlite3 в корне проекта)
        },
    }

# Настройки Twilio (или Plivo)
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = '+12513337680'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Создаем папку media в корне проекта

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
