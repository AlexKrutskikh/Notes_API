from rest_framework import serializers
from .models import Animal, AnimalPhoto
from django.core.validators import FileExtensionValidator


def validate_file_size(value):
    MAX_SIZE_MB = 10
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # 10 MB
    if value.size > MAX_SIZE_BYTES:
        raise serializers.ValidationError("InvalidFile.")
    return value


class AnimalSerializer(serializers.ModelSerializer):
    def validate_species(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("InvalidSpeciesName.")
        return value

    def validate_gender(self, value):
        if value not in ['male', 'female']:
            raise serializers.ValidationError("InvalidGender.")
        return value

    def validate_weight(self, value):
        try:
            weight = float(value)
            if weight <= 0:
                raise serializers.ValidationError("InvalidWeight.")
        except ValueError:
            raise serializers.ValidationError("InvalidWeight.")
        return value

    class Meta:
        model = Animal
        fields = [
            "species",
            "weight",
            "gender_choices",
            "is_homeless",
        ]

    def create(self, validated_data):
        user_id = self.context['user_id']
        animal_instance = Animal.objects.create(user_id=user_id, **validated_data)
        return animal_instance


class AnimalPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg'],
                message="InvalidFile"
            ),
            validate_file_size
        ]
    )

    class Meta:
        model = AnimalPhoto
        fields = ['photo']

    def create(self, validated_data):
        animal_instance = self.context['animal_instance']
        photo_instance = AnimalPhoto.objects.create(animal=animal_instance, **validated_data)
        return photo_instance
