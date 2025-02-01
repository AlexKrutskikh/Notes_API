from django.core.exceptions import ValidationError

"""Валидация данных"""


def validate_specialist_data(data):
    name = data.get("name", "").strip()
    last_name = data.get("last_name", "").strip()
    specialization = data.get("specialization", "").strip()
    animals = data.get("animals", "").strip()
    additional_info = data.get("additional_info", "").strip()
    telegram = data.get("telegram", "").strip()
    # Проверка имени
    if not name:
        raise ValidationError("Name is required.")
    if len(name) > 50:
        raise ValidationError("Name must be 50 characters or less.")

    # Проверка фамилии
    if not last_name:
        raise ValidationError("Last name is required.")
    if len(last_name) > 30:
        raise ValidationError("Last name must be 30 characters or less.")

    # Проверка специализации
    if not specialization:
        raise ValidationError("Specialization is required.")
    if len(specialization) > 255:
        raise ValidationError("Specialization must be 255 characters or less.")

    # Проверка животных
    if not animals:
        raise ValidationError("Animals is required.")
    if len(animals) > 255:
        raise ValidationError("Animals must be 255 characters or less.")

    # Проверка Telegram
    if not telegram:
        raise ValidationError("Telegram is required.")
    if len(telegram) > 50:
        raise ValidationError("Telegram must be 255 characters or less.")

    # Проверка дополнительной информации (необязательное поле)
    if additional_info and len(additional_info) > 500:
        raise ValidationError("Additional info must be 500 characters or less.")

    return {
        "name": name,
        "last_name": last_name,
        "specialization": specialization,
        "animals": animals,
        "additional_info": additional_info,
        "telegram": telegram,
    }
