from django.db import models

from apps.auth.models import User

"""Модель данных для хранения информации о специалисте"""


class Specialist(models.Model):
    SPECIALIST_INFO_FILL = "Specialist_info_fill"
    SPECIALIST_VERIFICATION = "Specialist_verification"

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=255)
    animals = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True)
    telegram = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, related_name="specialist", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default=SPECIALIST_INFO_FILL)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.specialization}"


"""Модель данных для хранения файлов документов специалиста"""


class SpecialistDocument(models.Model):
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="specialist_file_user", on_delete=models.CASCADE)
    specialists = models.ManyToManyField(Specialist, related_name="related_documents", blank=True)

    def __str__(self):
        return f"Document for {self.specialists.all()}"
