from rest_framework import serializers
from .models import Verify_code

class UpdateVerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify_code
        fields = ['phone', 'email', 'verify_code']
