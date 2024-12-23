from django.core.exceptions import ValidationError

"""Валидация данных"""


def validate_question_data(data):

    text = data.get("text", "").strip()
    if not text or len(text) > 4000:
        raise ValidationError("InvalidText")

    file_ids = data.get("file_ids")
    if not isinstance(file_ids, list):
        raise ValidationError("InvalidFile_ids")

    if not all(isinstance(id, int) and id > 0 for id in file_ids):
        raise ValidationError("InvalidFile_ids")

    animal_id = data.get("animal_id")

    if not animal_id:
        raise ValidationError("InvalidAnimal_id")

    if not isinstance(animal_id, int) or animal_id <= 0:
        raise ValidationError("InvalidAnimal_id")

    return data
