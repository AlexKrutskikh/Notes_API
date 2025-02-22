from django.db import models

from apps.auth.models import User

"""Модель данных для хранения информации о животных"""


class Animal(models.Model):

    gender_choices = [
        ("male", "male"),
        ("female", "female"),
    ]

    species = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=10, choices=gender_choices)
    is_homeless = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="animal_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
