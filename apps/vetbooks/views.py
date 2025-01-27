from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

"""Сохранение в БД данных о веткнижке"""

class CreateVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.id


        return Response({"message": "Vetbook created successfully"}, status=status.HTTP_201_CREATED)
