from rest_framework import serializers
from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Animal
        fields = ['name', 'species', 'gender', 'weight', 'is_homeless']




