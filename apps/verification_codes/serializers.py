from rest_framework import serializers

from apps.verification_codes.models import SmsCode


class UpdateVerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ["phone", "email", "verify_code"]


class SMSVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)
