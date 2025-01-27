from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile
from apps.animals.models import Animal


class Vetbook(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Владелец ветеринарной книжки (связь с Profile)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="animal_vetbook") # Паспорт животного (связь с Animal)

class Identification(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_identifications") # Веткнижка
    chip_number = models.CharField(max_length=50, blank=True, null=True)  # Номер чипа
    clinic_name = models.CharField(max_length=255, blank=True, null=True)  # Клиника установки чипа
    chip_installation_location = models.CharField(max_length=255, blank=True, null=True)  # Место установки чипа
    chip_installation_date = models.DateField(blank=True, null=True)  # Дата установки чипа


class Vaccination(models.Model):

    class Type(models.TextChoices):

            DEHELMINTHIZATION = "DEHELMINTHIZATION", _("Dehelminthization")
            RABIES = "RABIES", _("Rabies")
            OTHER = "OTHER", _("Other")

    type = models.CharField(
        max_length=50,
        choices=Type,
        default=Type.IN_PROGRESS,
    )

    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_vaccinations") # Веткнижка
    vaccine_name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=50)  # Серия
    expiration_date = models.DateField()  # Срок годности
    clinic_name = models.CharField(max_length=255) # Название клиники
    administration_date = models.DateField()  # Дата вакцинации
    validity_date = models.DateField()  # Срок окончания действия

class Procedure(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_procedures") # Веткнижка
    medication = models.CharField(max_length=50) # Препарат
    processing_date = models.DateField() # Дата обработки
    clinic_name = models.CharField(max_length=255, blank=True, null=True) # Название клиники

class ClinicalExamination(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="evetbook_examinations")
    examination_date = models.DateField()
    results = models.TextField(max_length=255, blank=True, null=True)
    files_ids = models.JSONField(blank=True, null=True)


class Registration(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_registration") # Веткнижка
    clinic_name = models.CharField(max_length=255, blank=True, null=True) # Название клиники
    registration_number = models.CharField(max_length=50, blank=True, null=True)  # Номер регистрации
