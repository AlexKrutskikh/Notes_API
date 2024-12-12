from django.db import models
from apps.auth.models import User

class Animal(models.Model):

    gender_choices = [

        ('male', 'male'),
        ('female', 'female'),
    ]

    name = models.CharField(max_length=20)
    species = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=10, choices=gender_choices)
    is_homeless = models.BooleanField()
    time_creation = models.DateTimeField(auto_now_add=True)
    time_change = models.DateTimeField(null=True)
    user = models.ForeignKey(User, related_name='animal_user', on_delete=models.CASCADE)


class AnimalPhoto(models.Model):
    animal= models.ForeignKey(Animal, related_name='animal_files', on_delete=models.CASCADE)
    photo = models.FileField(upload_to='animal_files/')