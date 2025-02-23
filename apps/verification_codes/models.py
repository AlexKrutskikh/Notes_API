from django.db import models


class VerificationCode(models.Model):
    code = models.CharField(max_length=6, unique=True)  # Уникальный код
    is_used = models.BooleanField(default=False)  # Статус использования
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"Code {self.code} - {'Used' if self.is_used else 'Available'}"
