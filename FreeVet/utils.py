from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

from apps.questions.models import QuestionFile

"""
   Функция для сохранения и валидации файлов  в указанное место и возвратом URL-ов.

   :param request: Django запрос, содержащий файлы.
   :param upload_path: Путь, куда нужно сохранить файлы.
   :return: Список URL-ов на сохраненные файлы или Response с ошибкой.
   """


def validate_file(file):
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("FileTooLarge")

    extension_validator = FileExtensionValidator(
        allowed_extensions=["jpg", "jpeg", "png"], message="InvalidFileExtension"
    )
    extension_validator(file)

    return file


def save_files_to_storage(request, upload_path):
    files = request.FILES.getlist("photos")

    if not files:
        raise ValidationError("No files uploaded")

    file_paths = []

    for file in files:
        try:
            validate_file(file)
            file_path = default_storage.save(f"{upload_path}/{file.name}", ContentFile(file.read()))
            file_paths.append(file_path)
        except Exception:
            raise ValidationError(f"Invalid file: {file.name}")

    return file_paths
