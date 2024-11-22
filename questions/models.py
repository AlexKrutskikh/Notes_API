from django.db import models
from django.utils.translation import gettext_lazy as _


"""Question model"""

class Question(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", _("InProgress")
        COMPLETED = "COMPLETED", _("Completed")

    status = models.CharField(
        max_length=50,
        choices=Status,
        default=Status.IN_PROGRESS,
    )

    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=100)
    vet_user_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.question


class QuestionFile(models.Model):
    question = models.ForeignKey(Question, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='questions_files/')

