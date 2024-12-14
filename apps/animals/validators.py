from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

"""
Функции для валидации различных данных: имени, вида, пола, веса и файлов.

- `validate_name(value)`: проверяет, что имя не содержит цифр.
- `validate_species(value)`: проверяет, что вид не содержит цифр.
- `validate_gender(value)`: проверяет, что пол соответствует 'male' или 'female'.
- `validate_weight(value)`: проверяет, что вес — это положительное число.
- `validate_file(file)`: проверяет размер файла и его расширение.
-  validate_is_homeless: проверяет, что поле соответствует True или False
"""


def validate_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("InvalidName")
    return value


def validate_species(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("InvalidSpecies")
    return value


def validate_gender(value):
    if value not in ['male', 'female']:
        raise ValidationError("InvalidGender")
    return value


def validate_weight(value):
    try:
        weight = float(value)
        if weight <= 0:
            raise ValidationError("InvalidWeight")
    except (ValueError, TypeError):
        raise ValidationError("InvalidWeight")
    return weight

def validate_is_homeless(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValidationError("InvalidIsHomeless")


def validate_file(file):

    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("FileTooLarge")


    extension_validator = FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'],
        message="InvalidFileExtension"
    )
    extension_validator(file)

    return file
