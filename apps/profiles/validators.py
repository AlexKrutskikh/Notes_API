from rest_framework.exceptions import ValidationError

"""
  Валидирует все роли в полученных данных.
  Ожидает, что значения всех ключей являются булевыми.
  """
def validate_roles(data):

    roles = {
        "Homeless_Helper": data.get("Homeless_Helper"),
        "Pers_Helper": data.get("Pers_Helper"),
        "Volunteer": data.get("Volunteer"),
        "Shelter_Worker": data.get("Shelter_Worker"),
        "Pet_Owner": data.get("Pet_Owner"),
        "Vet": data.get("Vet"),
        "Dog_Handler": data.get("Dog_Handler"),
        "Zoo_psychologist": data.get("Zoo_psychologist"),
    }

    for role, value in roles.items():
        if not isinstance(value, bool):
            raise ValidationError({role: f"Invalid value for {role}, expected a boolean."})

    return roles
