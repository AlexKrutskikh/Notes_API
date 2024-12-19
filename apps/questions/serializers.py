from rest_framework import serializers
from .models import Question

"Сериализатор для данных о вопросе"

class QuestionSerializer(serializers.ModelSerializer):


    class Meta:

        model = Question
        fields =  ['text', 'animal', 'file_ids']