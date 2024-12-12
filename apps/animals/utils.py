from rest_framework import serializers

def validate_file_size(value):
    MAX_SIZE_MB = 10
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # 10 MB
    if value.size > MAX_SIZE_BYTES:
        raise serializers.ValidationError("InvalidFile.")
    return value