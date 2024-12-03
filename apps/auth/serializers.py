from rest_framework import serializers

from apps.auth.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)

    class Meta:
        model = Profile
        fields = ['phone']

