from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.animals.models import Animal
from apps.auth.models import User

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

    text = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="question_user", on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, related_name="question_animal", on_delete=models.CASCADE)
    file_ids = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.question


"""Модель данных для хранения файлов"""


class QuestionFile(models.Model):
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="question_file_user", on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name="related_files", blank=True)
