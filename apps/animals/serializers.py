from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):

    gender = serializers.CharField()

    class Meta:
        model = Animal
        fields = ['name', 'species', 'gender', 'weight', 'is_homeless']

    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError("InvalidName")
        return value

    def validate_species(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError("InvalidSpecies")
        return value

    def validate_gender(self, value):
        if value not in ['male', 'female']:
            raise ValidationError("InvalidGender")
        return value

    def validate_weight(self, value):
        try:
            weight = float(value)
            if weight <= 0:
                raise ValidationError("InvalidWeight")
        except (ValueError, TypeError):
            raise ValidationError("InvalidWeight")
        return weight

    def validate_is_homeless(self, value):
        if isinstance(value, bool):
            return value  # Return boolean value as is

        if isinstance(value, str):
            lower_value = value.lower()
            if lower_value == 'true':
                return True
            elif lower_value == 'false':
                return False
            else:

                raise serializers.ValidationError("InvalidIsHomeless")

        raise serializers.ValidationError("InvalidIsHomeless")



