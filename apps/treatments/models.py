from django.db import models

from apps.vetbooks.models import Vetbook

class Treatment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="extended_treatments")
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    missed_doses = models.CharField(max_length=100, blank=True, null=True)
    calendar = models.TextField(blank=True, null=True)