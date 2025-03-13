from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

from django.utils.text import slugify
import time

"""
   Функция для сохранения и валидации файлов  в указанное место и возвратом URL-ов.

   :param request: Django запрос, содержащий файлы.
   :param upload_path: Путь, куда нужно сохранить файлы.
   :return: Список URL-ов на сохраненные файлы или Response с ошибкой.
   """


def validate_photo(photo):
    max_size_mb = 10
    if photo.size > max_size_mb * 1024 * 1024:
        raise ValidationError("PhotoTooLarge")

    extension_validator = FileExtensionValidator(
        allowed_extensions=["jpg", "jpeg", "png"], message="InvalidFileExtension"
    )
    extension_validator(photo)

    return photo

def validate_documents(file):
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("FileTooLarge")

    extension_validator = FileExtensionValidator(
        allowed_extensions=["jpg", "jpeg", "png", "pdf"], message="InvalidFileExtension"
    )
    extension_validator(file)

    return file


def save_files_to_storage(request, upload_path):
    photos = request.FILES.getlist("photos")
    files = request.FILES.getlist("files")

    if not photos and not files:
        raise ValidationError("No files uploaded.")

    file_paths = []

    # Process and validate photos
    for photo in photos:
        try:
            validate_photo(photo)  # Validate photo
            safe_filename = f"{slugify(photo.name)}_{int(time.time())}"  # Avoid duplicates
            file_path = default_storage.save(f"{upload_path}/{safe_filename}", ContentFile(photo.read()))
            file_paths.append(file_path)
        except Exception as e:
            raise ValidationError(f"Invalid photo '{photo.name}': {str(e)}")

    # Process and validate files (documents)
    for file in files:
        try:
            validate_documents(file)  # Validate documents
            safe_filename = f"{slugify(file.name)}_{int(time.time())}"  # Avoid duplicates
            file_path = default_storage.save(f"{upload_path}/{safe_filename}", ContentFile(file.read()))
            file_paths.append(file_path)
        except Exception as e:
            raise ValidationError(f"Invalid file '{file.name}': {str(e)}")

    return file_paths
