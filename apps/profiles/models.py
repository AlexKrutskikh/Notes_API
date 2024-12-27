from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.auth.models import User


class Profile(models.Model):

    class Perks(models.TextChoices):
        HOMELESS_HELPER = "PH", _("Homeless_Helper")
        PETS_HELPER = "HH", _("Pers_Helper")
        VOLUNTEER = "VR", _("Volunteer")
        SHELTER_WORKER = "SW", _("Shelter_Worker")
        PET_OWNER = "PO", _("Pet_Owner")
        VET = "VT", _("Vet")
        DOG_HANDLER = "DH", _("Dog_Handler")
        ZOO_PSYCHOLOGIST = "ZP", _("Zoo_psychologist")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    telegram = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    perks = models.TextField(choices=Perks.choices, default=Perks.HOMELESS_HELPER)
