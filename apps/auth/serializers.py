import re

from rest_framework import serializers

from apps.auth.models import SmsCode

"""Сериализатор для отправки и проверки SMS-кода.
    Поля:
        phone (CharField): Обязательное поле для номера телефона. Максимальная длина — 15 символов.
        code (CharField): Необязательное поле для кода. Должно состоять из 6 цифр.
"""


class SendSmsCodeSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(
        max_length=15,
        error_messages={"max_length": "WrongPhone", "blank": "WrongPhone"},
    )
    code = serializers.CharField(
        max_length=6,
        required=False,
        allow_blank=True,
        error_messages={"invalid": "InvalidCode", "blank": "InvalidCode"},
    )

    class Meta:
        model = SmsCode
        fields = ["phone", "code"]

    def validate(self, attrs):
        phone = attrs.get("phone")
        code = attrs.get("code")

        if not re.match(r"^\+\d{5,15}$", phone):
            raise serializers.ValidationError({"phone": "WrongPhone"})

        if code and not re.match(r"^\d{6}$", code):
            raise serializers.ValidationError({"code": "InvalidCode"})

        return attrs
