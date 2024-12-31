from django.db import models

from apps.auth.models import User

"""Модель для хранения перков"""


class Perks(models.Model):

    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


"""Модель для хранения профиля"""


class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    telegram = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True)
    path_photo = models.CharField(max_length=255)
    perks = models.ManyToManyField(Perks, blank=True)

    def __str__(self):
        return self.name
