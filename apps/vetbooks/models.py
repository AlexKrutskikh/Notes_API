from django.db import models

from apps.animals.models import Animal
from apps.auth.models import User


class Vetbook(models.Model):
    gender_choices = [
        ("male", "male"),
        ("female", "female"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец ветеринарной книжки (связь с Profile)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)  # Животное
    name = models.CharField(max_length=20)  # Имя
    photos_paths = models.JSONField(blank=True, null=True)  # Фото


class AdditionalDescription(models.Model):
    vetbook = models.ForeignKey(
        Vetbook, on_delete=models.CASCADE, related_name="vetbook_additional_description"
    )  # Веткнижка
    breed = models.CharField(max_length=20)  # Порода
    color = models.CharField(max_length=20)  # Окрас
    birth_date = models.DateField()  # Дата рождения
    special_marks = models.CharField(max_length=20)  # Особые приметы


class Identification(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_identification")  # Веткнижка
    chip_number = models.CharField(max_length=35)  # Номер чипа
    clinic = models.CharField(max_length=20)  # Клиника установки чипа
    chip_installation_location = models.CharField(max_length=20)  # Место установки чипа
    date = models.DateField()  # Дата установки чипа


class VaccinationAgainstRabies(models.Model):
    vetbook = models.ForeignKey(
        Vetbook, on_delete=models.CASCADE, related_name="vetbook_other_vaccinations"
    )  # Веткнижка
    vaccine = models.CharField(max_length=20)
    series = models.CharField(max_length=20)  # Серия
    expiration_date = models.DateField()  # Срок годности
    vaccination_clinic = models.CharField(max_length=20)  # Название клиники
    date_of_vaccination = models.DateField()  # Дата вакцинации
    vaccine_expiration_date = models.DateField()  # Срок окончания действия


class VaccinationOthers(models.Model):
    vetbook = models.ForeignKey(
        Vetbook, on_delete=models.CASCADE, related_name="vetbook_vaccination_against_rabies"
    )  # Веткнижка
    vaccine = models.CharField(max_length=20)
    series = models.CharField(max_length=20)  # Серия
    expiration_date = models.DateField()  # Срок годности
    vaccination_clinic = models.CharField(max_length=20)  # Название клиники
    date_of_vaccination = models.DateField()  # Дата вакцинации
    vaccine_expiration_date = models.DateField()  # Срок окончания действия


class Deworming(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_deworming")  # Веткнижка
    drug = models.CharField(max_length=35)  # Препарат
    date = models.DateField()  # Дата
    clinic = models.CharField(max_length=35)  # Название клиники


class EctoparasiteTreatment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_ectoparasite_treatment")  # Веткнижка
    drug = models.CharField(max_length=35)  # Препарат
    date = models.DateField()  # Дата обработки
    clinic = models.CharField(max_length=35)  # Название клиники


class ClinicalExamination(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_examinations")  # Веткнижка
    date = models.DateField()  # Дата осмотра
    result = models.TextField(max_length=20)  # Результаты
    files_ids = models.JSONField(blank=True, null=True)  # Файлы


class Registration(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_registration")  # Веткнижка
    clinic = models.CharField(max_length=20)  # Название клиники
    registration_number = models.CharField(max_length=35)  # Номер регистрации
