from django.db import models

from apps.auth.models import User

"""Модель данных для хранения информации о специалисте"""


class Specialist(models.Model):

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=255)
    animals = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True)
    telegram = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, related_name="specialist", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.specialization}"


"""Модель данных для хранения файлов документов специалиста"""


class SpecialistDocument(models.Model):
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="specialist_file_user", on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, related_name="related_documents", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Document for {self.specialist}"
