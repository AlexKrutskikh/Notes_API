from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import QuestionFile

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

def save_files_to_storage(request, upload_path, user_id):

    files = request.FILES.getlist('photos')

    if not files:
        raise ValidationError('No files uploaded')

    question_files = []

    for file in files:

        try:

            validate_file(file)
            file_path = default_storage.save(f"{upload_path}/{file.name}", ContentFile(file.read()))
            question_file = QuestionFile(path=file_path, user_id=user_id)
            question_files.append(question_file)

        except:

            raise ValidationError(f"Invalid file: {file.name}")

    return question_files







