from django.db import models

class Animal(models.Model):
    art = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    is_homeless = models.BooleanField()
