from enum import EnumType
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.db import models


"""User model"""

class User(models.Model):
    class UserType(models.TextChoices):
        CLIENT = 'CL', _('Client')
        SPECIALIST = 'SP', _('Specialist')

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    auth_provider = models.CharField(max_length=50, default='Twilio')                   # Социальная сеть
    registration_time = models.DateTimeField(auto_now_add=True)                         # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)                               # Время последнего входа
    email = models.EmailField(unique=True, blank=True, null=True)                       # Почта

    type = models.CharField(                                                            # Тип пользователя
        max_length=2,
        choices=UserType.choices,
        default=UserType.CLIENT,
    )
