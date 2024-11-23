from django.db import models
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):

    class Perks(models.TextChoices):
        HOMELESS_HELPER = 'PH', _('Homeless Helper')
        PETS_HELPER = 'HH', _('Pers Helper')
        VOLUNTEER = 'VR', _('Volunteer')
        SHELTER_WORKER = 'SW', _('Shelter Worker')
        PET_OWNER = 'PO', _('Pet Owner')
        VET = 'VT', _('Vet')
        DOG_HANDLER = 'DH', _('Dog Handler')
        ZOO_PSYCHOLOGIST = 'ZP', _('Zoopsychologist')

    name = models.CharField(max_length=50)                                              # Имя
    last_name = models.CharField(max_length=30, blank=True, null=True)                  # Фамилия
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)         # Фото
    perks = models.TextField(choices=Perks.choices, default=Perks.HOMELESS_HELPER)      # Перки
