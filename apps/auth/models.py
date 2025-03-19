from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

"""Кастомный менеджер пользователей для модели CustomUser.
    Позволяет создавать пользователей и суперпользователей.
    Этот менеджер переопределяет стандартные методы создания пользователя и суперпользователя,
    чтобы использовать email в качестве уникального идентификатора и автоматически нормализовать email"""


class UserManager(BaseUserManager):
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


"""Кастомная модель пользователя.
    Модель наследует от AbstractBaseUser для использования кастомной логики аутентификации и
    PermissionsMixin для поддержки разрешений и групп в Django"""


class User(AbstractBaseUser, PermissionsMixin):

    class UserRole(models.TextChoices):

        USER = "User"
        EDITOR = "Editor"

    auth_provider = models.CharField(max_length=50, default="RegistrationUser")
    registration_time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True)

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
