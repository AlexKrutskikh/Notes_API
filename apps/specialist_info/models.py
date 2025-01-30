from django.db import models

from apps.auth.models import User


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="specialist")
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    document = models.FileField(upload_to="specialist_documents/")
    specialization = models.CharField(max_length=255)
    animals = models.CharField(max_length=255)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.specialization}"
