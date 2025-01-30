from django.db import models

from apps.auth.models import User

"""Модель данных для хранения информации о животных"""


class Animal(models.Model):

    gender_choices = [
        ("male", "male"),
        ("female", "female"),
    ]

    species = models.CharField(max_length=20)  # Вид
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Вес
    gender = models.CharField(max_length=10, choices=gender_choices)  # Пол
    is_homeless = models.BooleanField()  # Бездомность
    user = models.ForeignKey(User, related_name="user_animals", on_delete=models.CASCADE)
