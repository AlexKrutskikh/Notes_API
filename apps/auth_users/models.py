from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        CLIENT = 'CL', _('Client')
        SPECIALIST = 'SP', _('Specialist')

    password = None
    auth_provider = models.CharField(max_length=50, default='Twilio')  # Социальная сеть
    registration_time = models.DateTimeField(auto_now_add=True)        # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)              # Время последнего входа
    email = models.EmailField(unique=True, blank=True, null=True)      # Почта
    type = models.CharField(                                           # Тип пользователя
        max_length=2,
        choices=UserType.choices,
        default=UserType.CLIENT,
    )

    is_active = models.BooleanField(default=True)  # Поле активности пользователя
    is_staff = models.BooleanField(default=False)  # Поле персонала

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
