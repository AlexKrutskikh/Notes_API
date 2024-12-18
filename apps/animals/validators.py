from django.core.exceptions import ValidationError
import re


def validate_animal_data(data):

    if re.search(r'\d', data.get('name', '')):
        raise ValidationError("InvalidName")


    if re.search(r'\d', data.get('species', '')):
        raise ValidationError("InvalidSpecies")


    gender = data.get('gender')
    if gender not in ['male', 'female']:
        raise ValidationError("InvalidGender")


    weight_str = data.get('weight', '')
    try:
        weight = float(weight_str)
        if weight <= 0:
            raise ValidationError("InvalidWeight")
    except ValueError:
        raise ValidationError("InvalidWeight")


    is_homeless_str = data.get('is_homeless', '').lower()
    if is_homeless_str not in ['true', 'false']:
        raise ValidationError("InvalidIsHomeless")

    return data
