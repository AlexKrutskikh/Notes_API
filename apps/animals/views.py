from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import Animal
from .serializers import AnimalSerializer


class AddAnimalAPIView(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        serializer = AnimalSerializer(data=request.data)

        if serializer.is_valid():

            validated_data = serializer.validated_data
            animal = Animal.objects.create(
                user_id=user_id,
                **validated_data
            )

            return Response({
                'message': 'Successfully created',
                'id_animal': animal.id
            }, status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
