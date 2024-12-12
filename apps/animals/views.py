from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .serializers import AnimalSerializer, AnimalPhotoSerializer

"""Обрабатывает создание новой записи `Animal` и связанных фотографий"""

class AddAnimalAPIView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user_id = request.user.id

        serializer = AnimalSerializer(data=request.data, context={'user_id': user_id})

        if serializer.is_valid():
            animal_instance = serializer.save()


            files = request.FILES.getlist('photos')
            if files:
                photo_serializer = AnimalPhotoSerializer(
                    data={'photos': files},
                    context={'animal_instance': animal_instance}
                )
                if photo_serializer.is_valid():
                    photo_serializer.save()
                else:

                    return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
