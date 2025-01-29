from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.auth.models import User
from apps.animals.models import Animal


class Vetbook(models.Model):
    gender_choices = [
        ("male", "male"),
        ("female", "female"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец ветеринарной книжки (связь с Profile)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE) # Животное
    name = models.CharField(max_length=20)  # Имя
    photosPaths = models.JSONField(blank=True, null=True) # Фото



class AdditionalDescription(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_additionalDescription")  # Веткнижка
    breed = models.CharField(max_length=20)  # Порода
    color =  models.CharField(max_length=20)  # Окрас
    birthDate = models.DateField()  # Дата рождения
    specialMarks = models.CharField(max_length=20)  # Особые приметы

class Identification(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_identifications")  # Веткнижка
    chipNumber = models.CharField(max_length=35)  # Номер чипа
    clinic = models.CharField(max_length=20)  # Клиника установки чипа
    locationInstallChip = models.CharField(max_length=20)  # Место установки чипа
    chipDate = models.DateField()  # Дата установки чипа


class VaccinationAgainstRabies(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_vaccinationAgainstRabies")  # Веткнижка
    vaccine = models.CharField(max_length=20)
    series = models.CharField(max_length=20)  # Серия
    expirationDate = models.DateField()  # Срок годности
    vaccinationClinic = models.CharField(max_length=20)  # Название клиники
    dateOfVaccination = models.DateField()  # Дата вакцинации
    vaccineExpirationDate = models.DateField()  # Срок окончания действия

class VaccinationOthers(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_vaccinationOthers")  # Веткнижка
    vaccine = models.CharField(max_length=20)
    series = models.CharField(max_length=20)  # Серия
    expirationDate = models.DateField()  # Срок годности
    vaccinationClinic = models.CharField(max_length=20)  # Название клиники
    dateOfVaccination = models.DateField()  # Дата вакцинации
    vaccineExpirationDate = models.DateField()  # Срок окончания действия

class Deworming(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_deworming")  # Веткнижка
    dewormingDrug = models.CharField(max_length=35)  # Препарат
    dewormingDate = models.DateField()  # Дата
    dewormingClinic = models.CharField(max_length=35)  # Название клиники


class EctoparasiteTreatment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_procedures")  # Веткнижка
    ectoparasitesDrug = models.CharField(max_length=35)  # Препарат
    ectoparasitesDate = models.DateField()  # Дата обработки
    ectoparasitesClinic = models.CharField(max_length=35)  # Название клиники


class ClinicalExamination(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_examinations") # Веткнижка
    date = models.DateField() # Дата осмотра
    result = models.TextField(max_length=20) # Результаты
    files_ids = models.JSONField(blank=True, null=True) # Файлы


class Registration(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_registration")  # Веткнижка
    clinic = models.CharField(max_length=20)  # Название клиники
    registrationNumber = models.CharField(max_length=35)  # Номер регистрации


# class Treatment(models.Model):
#     vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_treatments")
#     medication = models.CharField(max_length=255)
#     dosage = models.CharField(max_length=100)
#     frequency = models.CharField(max_length=100)
#     startDate = models.DateField()
#     endDate = models.DateField()
#     calendar = models.JSONField(blank=True, null=True)  # Массив дат


# class Appointment(models.Model):
#     vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_appointments")
#     clinic_name = models.CharField(max_length=255)
#     visit_date = models.DateField()
#     complaints = models.TextField(max_length=255, blank=True, null=True)
#     doctor_report = models.TextField(max_length=255, blank=True, null=True)
#     examination_files_ids = models.JSONField(blank=True, null=True)
#     other_files_ids = models.JSONField(blank=True, null=True)
