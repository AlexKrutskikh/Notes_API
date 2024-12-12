from rest_framework import serializers
from .models import Animal, AnimalPhoto
from django.core.validators import FileExtensionValidator
from .utils import validate_file_size
import re

"""Сериализаторы в данном коде используются для валидации и обработки данных,
 связанных с моделями Animal и AnimalPhoto. Код включает пользовательские проверки, 
 чтобы гарантировать, что данные соответствуют ожидаемому формату перед их сохранением в базу данных. 
 Функция create используется для создания экземпляров моделей и интеграции их с дополнительными данными из контекста."""

class AnimalSerializer(serializers.ModelSerializer):

    weight = serializers.FloatField(
        error_messages={
            'invalid': "InvalidWeight",
            'required': "InvalidWeight",
        }
    )

    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("InvalidName")
        return value

    def validate_species(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("InvalidSpeciesName")
        return value

    def validate_gender(self, value):
        if value not in ['male', 'female']:
            raise serializers.ValidationError("InvalidGender")
        return value

    def validate_weight(self, value):
        try:
            weight = float(value)
            if weight <= 0:
                raise serializers.ValidationError("InvalidWeight")
        except (ValueError, TypeError):
            raise serializers.ValidationError("InvalidWeight")
        return weight

    class Meta:
        model = Animal
        fields = [
            "name",
            "species",
            "weight",
            "gender",
            "is_homeless",
        ]

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Animal.objects.create(user_id=user_id, **validated_data)

class AnimalPhotoSerializer(serializers.ModelSerializer):

        photos = serializers.ListField(
            child=serializers.ImageField(
                validators=[
                    FileExtensionValidator(
                        allowed_extensions=['jpg', 'jpeg'],
                        message="InvalidFile"
                    ),
                    validate_file_size
                ]
            ),
            required=True
        )

        class Meta:
            model = AnimalPhoto
            fields = ['photos']

        def create(self, validated_data):
            animal_instance = self.context['animal_instance']
            photos = validated_data.get('photos', [])
            return [AnimalPhoto.objects.create(animal=animal_instance, photo=photo) for photo in photos]
