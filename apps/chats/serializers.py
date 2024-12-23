from rest_framework import serializers

from apps.chats.models import Message, MessageFile


class MessageFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()  # Поле для полного URL файла

    class Meta:
        model = MessageFile
        fields = ["file_url"]  # Включаем только поле с URL файла

    def get_file_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url


class MessageSerializer(serializers.ModelSerializer):
    files = MessageFileSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
