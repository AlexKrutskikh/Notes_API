from rest_framework import serializers
from apps.auth.models import SmsCode
import re

"""Сериализатор используется для получения и валидации номера телефона,
    с последующей отправкой SMS-кода для регистрации или аутентификации пользователя."""


class SendSmsCodeSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(max_length=15)

    class Meta:
        model = SmsCode
        fields = ['phone']

    def validate_phone(self, value):
        if not re.match(r'^\d{10,15}$', value):
            raise serializers.ValidationError("Введите корректный номер телефона (10-15 цифр).")
        return value

