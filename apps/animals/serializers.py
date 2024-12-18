from rest_framework import serializers
from .models import Animal

"Сериализатор для данных о животном"

class AnimalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Animal
        fields = ['name', 'species', 'gender', 'weight', 'is_homeless']




