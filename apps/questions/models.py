from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.auth.models import User
from apps.animals.models import Animal

"""Модель данных для хранения информации о вопросах"""

class Question(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", _("InProgress")
        COMPLETED = "COMPLETED", _("Completed")

    status = models.CharField(
        max_length=50,
        choices=Status,
        default=Status.IN_PROGRESS,
    )

    question = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='question_user', on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, related_name='question_animal', on_delete=models.CASCADE)


    def __str__(self):
        return self.question


class QuestionFile(models.Model):
    file = models.FileField(upload_to='questions_files/')

