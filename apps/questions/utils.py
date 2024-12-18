from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from rest_framework import status
from rest_framework.response import Response

"""
   Функция для сохранения и валидации файлов  в указанное место и возвратом URL-ов.

   :param request: Django запрос, содержащий файлы.
   :param upload_path: Путь, куда нужно сохранить файлы.
   :return: Список URL-ов на сохраненные файлы или Response с ошибкой.
   """

def validate_file(file):

    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("FileTooLarge")


    extension_validator = FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'],
        message="InvalidFileExtension"
    )
    extension_validator(file)

    return file

def save_files_to_storage(request, upload_path):

    photo_urls = []

    files = request.FILES.getlist('photos')

    for file in files:
        try:
            validate_file(file)
            file_path = default_storage.save(f"{upload_path}/{file.name}", ContentFile(file.read()))
            file_url = default_storage.url(file_path)
            photo_urls.append(file_url)

        except ValidationError:
            return Response({'error': 'Invalid file(s)'}, status=status.HTTP_400_BAD_REQUEST)

    if not photo_urls:
        return Response({'error': 'Invalid file(s)'}, status=status.HTTP_400_BAD_REQUEST)

    return photo_urls