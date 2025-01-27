from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .validators import validate_identification_data
from .models import Vetbook, Identification

"""Сохранение в БД данных о веткнижке"""

class CreateVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.id


        return Response({"message": "Vetbook created successfully"}, status=status.HTTP_201_CREATED)
    

"""Сохранение в БД данных о идентификации в веткнижке и возврат ее id"""

class AddIdentification(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # CAN WE GET VETBOOK ID LIKE request.data.vetbook_id or request.data.get("vetbook_id", "")
        data = request.data
        try:
            validated_data = validate_identification_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        vetbook = Vetbook.objects.get(id=request.data.get("vetbook_id", ""))
    
        if not vetbook:
            return Response(
                {
                    "error": "VetbookNotFound",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            identification = Identification.objects.create(
                vetbook=vetbook,
                chip_number=validated_data.get("chip_number"),
                clinic_name=validated_data.get("clinic_name"),
                chip_installation_location=validated_data.get("chip_installation_location"),
                chip_installation_date=validated_data.get("chip_installation_date")
            )
            return Response({"message": "Identification for a vetbook created successfully", "identification_id": identification.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
