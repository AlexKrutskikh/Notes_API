from rest_framework.exceptions import ValidationError

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
