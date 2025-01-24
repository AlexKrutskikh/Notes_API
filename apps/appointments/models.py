from django.db import models

from apps.vetbooks.models import Vetbook

class Appointment(models.Model):
    vetbook = models.ForeignKey(Vetbook, on_delete=models.CASCADE, related_name="vetbook_appointments")
    clinic_name = models.CharField(max_length=255)
    visit_date = models.DateField()
    complaints = models.TextField(blank=True, null=True)
    doctor_report = models.TextField(blank=True, null=True)
    examination_files_ids = models.JSONField(blank=True, null=True)
    other_files_ids = models.JSONField(blank=True, null=True)
