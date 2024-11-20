from django.db import models


class Profile(models.Model):

    homelessAnimals = models.BooleanField(default=False)  # Бездомные животные
    pets = models.BooleanField(default=False)             # Домашние животные
    volunteer = models.BooleanField(default=False)        # Волонтер
    shelterWorker = models.BooleanField(default=False)    # Работник приюта