import re

from rest_framework.exceptions import ValidationError

"""
  Валидирует все роли в полученных данных.
  Ожидает, что значения всех ключей являются булевыми.
  """


def validate_perk(data):

    role_mapping = {
        "Homeless_Helper": "Client",
        "Pers_Helper": "Client",
        "Volunteer": "Client",
        "Shelter_Worker": "Client",
        "Pet_Owner": "Client",
        "Vet": "Specialist",
        "Dog_Handler": "Specialist",
        "Zoo_psychologist": "Specialist",
    }


    active_perks = []
    choice_role = None

    for perk_name, value in data.items():

        if not isinstance(value, bool):
            raise ValidationError(f"Invalid value for {perk_name}, expected a boolean.")

        if value:

            if choice_role is None:
                choice_role = role_mapping.get(perk_name)


            if role_mapping.get(perk_name) != choice_role:
                raise ValidationError("All selected perks must have the same role.")
            else:
                active_perks.append(perk_name)


    return active_perks, choice_role


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
