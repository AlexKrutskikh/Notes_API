from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["homelessAnimals", "pets", "volunteer", "shelterWorker", "petOwner"]


class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "photo", "volunteer", "shelterWorker", "petOwner", "pets", "homelessAnimals"]
