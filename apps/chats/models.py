from django.db import models

from apps.questions.models import Question


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=100, null=True)
    is_user = models.BooleanField(default=True)
    question = models.ForeignKey(Question, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class MessageFile(models.Model):
    message = models.ForeignKey(Message, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='messages_files/')
