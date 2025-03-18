from django.db import models

from apps.auth.models import User


class Notes(models.Model):

    title = models.CharField(max_length=20)
    body = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="note_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
