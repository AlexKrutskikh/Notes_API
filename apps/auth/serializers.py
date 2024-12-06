import re
from rest_framework import serializers
from apps.auth.models import SmsCode

"""Сериализатор для отправки и проверки SMS-кода.
    Поля:
        phone (CharField): Обязательное поле для номера телефона. Максимальная длина — 15 символов.
        code (CharField): Необязательное поле для кода. Должно состоять из 6 цифр.
"""

class SendSmsCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6, required=False, allow_blank=True)

    class Meta:
        model = SmsCode
        fields = ['phone', 'code']

    def validate_phone(self, value):

        if not re.match(r'^\+?\d{5,15}$', value):
            raise serializers.ValidationError({
                "error_type": "WrongPhone"
            })
        return value

    def validate_code(self, value):

        if value:
            if not re.match(r'^\d{6}$', value):
                raise serializers.ValidationError({
                    "error_type": "InvalidCode",
                })
        return value


