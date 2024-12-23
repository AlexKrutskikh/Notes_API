import re

from django.core.exceptions import ValidationError

"""Валидация данных животного"""


def validate_animal_data(data):

    if re.search(r"\d", data.get("name", "")):
        raise ValidationError("InvalidName")

    if re.search(r"\d", data.get("species", "")):
        raise ValidationError("InvalidSpecies")

    gender = data.get("gender")
    if gender not in ["male", "female"]:
        raise ValidationError("InvalidGender")

    weight_str = data.get("weight", "")
    try:
        weight = float(weight_str)
        if weight <= 0:
            raise ValidationError("InvalidWeight")
    except ValueError:
        raise ValidationError("InvalidWeight")

    is_homeless = data.get("is_homeless")
    if not isinstance(is_homeless, bool):
        raise ValidationError("InvalidIsHomeless")

    return data
