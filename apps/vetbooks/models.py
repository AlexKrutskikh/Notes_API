from django.db import models

from apps.animals.models import Animal
from apps.auth.models import User


class Vetbook(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец ветеринарной книжки (связь с Profile)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)  # Животное
    name = models.CharField(max_length=20)  # Имя
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(null=True, blank=True)  # Дата обновления
    files_ids = models.JSONField(blank=True, null=True)  # Фото


class VetbookFile(models.Model):
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="vetbook_file_user", on_delete=models.CASCADE)
    vetbooks = models.ManyToManyField(Vetbook, related_name="vetbook_related_files", blank=True)


class Vetpass(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbooks_vetpass")  # Веткнижка


class AdditionalDescription(models.Model):
    vetpass = models.ForeignKey(
        Vetpass, on_delete=models.CASCADE, related_name="vetpass_additional_description"
    )  # Ветпаспорт
    breed = models.CharField(max_length=20, blank=True, null=True)  # Порода
    color = models.CharField(max_length=20, blank=True, null=True)  # Окрас
    birth_date = models.DateField(blank=True, null=True)  # Дата рождения
    special_marks = models.CharField(max_length=20, blank=True, null=True)  # Особые приметы


class Identification(models.Model):
    vetpass = models.ForeignKey(Vetpass, on_delete=models.CASCADE, related_name="vetpass_identification")  # Ветпаспорт
    chip_number = models.CharField(max_length=35, blank=True, null=True)  # Номер чипа
    clinic = models.CharField(max_length=20, blank=True, null=True)  # Клиника установки чипа
    chip_installation_location = models.CharField(max_length=20, blank=True, null=True)  # Место установки чипа
    date = models.DateField(blank=True, null=True)  # Дата установки чипа


class VaccinationAgainstRabies(models.Model):
    vetpass = models.ForeignKey(
        Vetpass, on_delete=models.CASCADE, related_name="vetpass_other_vaccinations"
    )  # Ветпаспорт
    vaccine = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=20, blank=True, null=True)  # Серия
    expiration_date = models.DateField(blank=True, null=True)  # Срок годности
    vaccination_clinic = models.CharField(max_length=20, blank=True, null=True)  # Название клиники
    date_of_vaccination = models.DateField(blank=True, null=True)  # Дата вакцинации
    vaccine_expiration_date = models.DateField(blank=True, null=True)  # Срок окончания действия


class VaccinationOthers(models.Model):
    vetpass = models.ForeignKey(
        Vetpass, on_delete=models.CASCADE, related_name="vetpass_vaccination_against_rabies"
    )  # Ветпаспорт
    vaccine = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=20, blank=True, null=True)  # Серия
    expiration_date = models.DateField(blank=True, null=True)  # Срок годности
    vaccination_clinic = models.CharField(max_length=20, blank=True, null=True)  # Название клиники
    date_of_vaccination = models.DateField(blank=True, null=True)  # Дата вакцинации
    vaccine_expiration_date = models.DateField(blank=True, null=True)  # Срок окончания действия


class Deworming(models.Model):
    vetpass = models.ForeignKey(Vetpass, on_delete=models.CASCADE, related_name="vetpass_deworming")  # Ветпаспорт
    drug = models.CharField(max_length=35, blank=True, null=True)  # Препарат
    date = models.DateField(blank=True, null=True)  # Дата
    clinic = models.CharField(max_length=35, blank=True, null=True)  # Название клиники


class EctoparasiteTreatment(models.Model):
    vetpass = models.ForeignKey(
        Vetpass, on_delete=models.CASCADE, related_name="vetpass_ectoparasite_treatment"
    )  # Ветпаспорт
    drug = models.CharField(max_length=35, blank=True, null=True)  # Препарат
    date = models.DateField(blank=True, null=True)  # Дата обработки
    clinic = models.CharField(max_length=35, blank=True, null=True)  # Название клиники


class ClinicalExamination(models.Model):
    vetpass = models.ForeignKey(Vetpass, on_delete=models.CASCADE, related_name="vetpass_examinations")  # Ветпаспорт
    date = models.DateField(blank=True, null=True)  # Дата осмотра
    result = models.TextField(max_length=20, blank=True, null=True)  # Результаты
    files_ids = models.JSONField(blank=True, null=True)  # Файлы


class Registration(models.Model):
    vetpass = models.ForeignKey(Vetpass, on_delete=models.CASCADE, related_name="vetpass_registration")  # Ветпаспорт
    clinic = models.CharField(max_length=20, blank=True, null=True)  # Название клиники
    registration_number = models.CharField(max_length=35, blank=True, null=True)  # Номер регистрации
