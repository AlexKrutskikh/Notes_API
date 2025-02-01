from django.db import models

from apps.auth.models import User

"""Модель данных для хранения информации о специалиста"""


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=255)
    animals = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True)
    telegram = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.specialization}"


"""Модель данных для хранения информации о документах специалиста"""


class SpecialistDocument(models.Model):
    document = models.FileField(upload_to="documents/")
    specialist = models.ForeignKey(Specialist, related_name="documents", on_delete=models.CASCADE)

    def __str__(self):
        return f"Document for {self.specialist}"
