from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import random



"""User model"""


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    auth_provider = models.CharField(max_length=50, default='Twilio')                   # Социальная сеть
    name = models.CharField(max_length=50)                                              # Имя
    registration_time = models.DateTimeField(auto_now_add=True)                         # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)                               # Время последнего входа
    is_user = models.BooleanField(default=False)                                        # Роль

    last_name = models.CharField(max_length=30, blank=True, null=True)                  # Фамилия
    phone = models.CharField(max_length=50, unique=True, blank=True, null=True)         # Номер телефона
    email = models.EmailField(unique=True, blank=True, null=True)                       # Почта
    verify_code = models.CharField(max_length=6, blank=True, null=True)



