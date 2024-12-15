from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import Animal
from .validators import (validate_name, validate_species, validate_gender,
validate_weight, validate_file, validate_is_homeless)
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

"""
API для добавления животного.

- Получает данные пользователя и проверяет их на валидность с использованием различных функций для валидации.
- Обрабатывает файлы изображений и проверяет их на допустимый размер и расширение.
- Сохраняет данные о животном и его фотографии в базу данных.
- Возвращает успешный ответ с идентификатором созданного объекта или ошибку при невалидных данных.

"""


class AddAnimalAPIView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.data


        try:
            validated_data = {
                'name': validate_name(data.get('name')),
                'species': validate_species(data.get('species')),
                'gender': validate_gender(data.get('gender')),
                'weight': validate_weight(data.get('weight')),
                'is_homeless': validate_is_homeless(data.get('is_homeless'))
            }
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        photo_urls = []
        files = request.FILES.getlist('photos')


        for file in files:

            try:
                validate_file(file)
                file_path = default_storage.save(f"animal_photos/{file.name}", ContentFile(file.read()))
                file_url = default_storage.url(file_path)
                photo_urls.append(file_url)

            except ValidationError:
                return Response({'error': 'Invalid file(s)'}, status=status.HTTP_400_BAD_REQUEST)


        if not photo_urls:
            return Response({'error': 'Invalid file(s)'}, status=status.HTTP_400_BAD_REQUEST)


        animal_instance = Animal.objects.create(
            user_id=user_id,
            photos=photo_urls,
            **validated_data
        )

        return Response({
            'message': 'Successfully created',
            'id_animal': animal_instance.id
        }, status=status.HTTP_201_CREATED)
