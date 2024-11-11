from django.db import models


"""Question model"""

class Question(models.Model):

    question = models.TextField()
    pet_art = models.CharField(max_length=100)
    pet_weight = models.CharField(max_length=100)
    pet_gender = models.CharField(max_length=50)
    is_homeless = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class QuestionFile(models.Model):
    question = models.ForeignKey(Question, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='questions_files/')


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=True)
    question = models.ForeignKey(Question, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class MessageFile(models.Model):
    message = models.ForeignKey(Message, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='messages_files/')