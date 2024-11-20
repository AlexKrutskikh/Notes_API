from rest_framework.views import APIView
from serializers import ProfileSerializer
from rest_framework.response import Response
from models import Profile
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

class UpdateProfileFieldsView(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем user_id из запроса
        user_id = request.data.get('user_id')
        if user_id is None:
            user_id = request.data.get('userId')
            if user_id is None:
                return Response(
                    {"detail": "Не заполнен параметр user_id."},
                    status=status.HTTP_400_BAD_REQUEST)

        # Ищем профиль с указанным user_id
        profile = get_object_or_404(Profile, user_id=user_id)

        # Десериализуем и проверяем данные
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            # Устанавливаем is_active в True
            serializer.validated_data['is_active'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST
