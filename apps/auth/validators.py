import re
from django.core.exceptions import ValidationError


def validate_phone_code(data):

    phone = data.get("phone", "")
    code = data.get("code", "")

    if not re.match(r"^\+\d{5,15}$", phone):
        raise ValidationError("WrongPhone")

    if code and not re.match(r"^\d{6}$", code):
        raise ValidationError("InvalidCode")

    return data