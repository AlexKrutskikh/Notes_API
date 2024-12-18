from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .validators import validate_animal_data
from .models import Animal
from .serializers import AnimalSerializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


"""Сохранение в БД данных о животном и возврат id"""
class AddAnimalAPIView(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):


        user_id = request.user.id
        data = request.data


        try:
            validated_data = validate_animal_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        serializer = AnimalSerializer(data=validated_data)

        if serializer.is_valid():

            try:
                animal = Animal.objects.create(
                    user_id=user_id,
                    **serializer.validated_data

                )
                return Response({
                    'message': 'Successfully created',
                    'id_animal': animal.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
