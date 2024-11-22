from django.db import models


class Аnimals(models.Model):

    pet_art = models.CharField(max_length=100)
    pet_weight = models.CharField(max_length=100)
    pet_gender = models.CharField(max_length=50)
    is_homeless = models.BooleanField()
