from rest_framework.exceptions import ValidationError
import re

"""
  Валидирует все роли в полученных данных.
  Ожидает, что значения всех ключей являются булевыми.
  """
def validate_perk(data):

    perk = {
        "Homeless_Helper": data.get("Homeless_Helper"),
        "Pers_Helper": data.get("Pers_Helper"),
        "Volunteer": data.get("Volunteer"),
        "Shelter_Worker": data.get("Shelter_Worker"),
        "Pet_Owner": data.get("Pet_Owner"),
        "Vet": data.get("Vet"),
        "Dog_Handler": data.get("Dog_Handler"),
        "Zoo_psychologist": data.get("Zoo_psychologist"),
    }

    for perk, value in perk.items():
        if not isinstance(value, bool):
            raise ValidationError({perk: f"Invalid value for {perk}, expected a boolean."})

    return data


def validate_user_data(data):
    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    telegram = data.get("telegram", "")


    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ]{2,}$", name):
        raise ValidationError("InvalidName")

    if not re.match(r"^\d{10,15}$", str(phone)):
        raise ValidationError("InvalidPhone")

    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValidationError("InvalidEmail")

    if telegram and not re.match(r"^[a-zA-Z]\w{4,31}$", telegram):
        raise ValidationError("InvalidTelegram")

    return data



