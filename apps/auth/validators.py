import re

from django.core.exceptions import ValidationError


def validate_user_data(data):
    phone = data.get("phone", "")
    email = data.get("email", "")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    username = data.get("username", "")
    password = data.get("password", "")

    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ-]{2,}$", first_name):
        raise ValidationError("InvalidFirstName")

    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ-]{2,}$", last_name):
        raise ValidationError("InvalidLastName")

    if not re.match(r"^[\w\d_-]{3,20}$", username):
        raise ValidationError("InvalidUserName")

    if not re.match(r"^\+?\d{10,15}$", str(phone)):
        raise ValidationError("InvalidPhone")

    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValidationError("InvalidEmail")

    password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,20}$"
    if not re.match(password_pattern, password):
        raise ValidationError(
            "Password must be 8-20 characters long and include uppercase, lowercase, a digit, and a special character."
        )

    return data
