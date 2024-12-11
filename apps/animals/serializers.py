from rest_framework import serializers
from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):

    def validate_species(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Invalid species name.")
        return value

    def validate_gender(self, value):
        if value not in ['male', 'female']:
            raise serializers.ValidationError("Invalid gender.")
        return value

    def validate_weight(self, value):
        try:
            weight = float(value)
            if weight <= 0:
                raise serializers.ValidationError("Invalid weight.")
        except ValueError:
            raise serializers.ValidationError("Invalid weight.")
        return value

    class Meta:
        model = Animal
        fields = [
            "species",
            "weight",
            "gender"
        ]
