from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.animals.models import Animal
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Vetbook
from .validators import validate_create_data

"""Сохранение в БД данных о веткнижке"""


class CreateVetbook(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.data

        try:
            photos_paths = save_files_to_storage(request, "vetbook_photos")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_data = validate_create_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            animal = Animal.objects.create(
                user=user,
                breed=validated_data.get("species"),
                gender=validated_data.get("gender"),
                weight=validated_data.get("weight"),
                isHomeless=validated_data.get("isHomeless"),
            )
            vetbook = Vetbook.objects.create(
                owner=user, name=validated_data.get("name"), animal=animal, photosPaths=photos_paths
            )

            return Response(
                {"message": "Vetbook created successfully", "vetbook_id": vetbook.id}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class VetbookInfo(APIView):
#     authentication_classes = [JWTTokenUserAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         vetbook_id = request.data.get("vetbook_id", "")
#         try:
#             vetbook = Vetbook.objects.prefetch_related(
#                 "vetbook_identifications",
#                 "vetbook_vaccinations",
#                 "vetbook_procedures",
#                 "vetbook_examinations",
#                 "vetbook_registration",
#                 "vetbook_treatments",
#                 "vetbook_appointments",
#             ).get(id=vetbook_id)

#             # Serialize the vetbook object
#             serializer = VetbookSerializer(vetbook)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# """Сохранение в БД данных о идентификации в веткнижке и возврат ее id"""


# class AddIdentification(APIView):

#     authentication_classes = [JWTTokenUserAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data
#         vetbook_id = request.data.get("vetbook_id", "")
#         try:
#             validated_data = validate_identification_data(data)
#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         vetbook = Vetbook.objects.get(id=vetbook_id)

#         if not vetbook:
#             return Response(
#                 {
#                     "error": "VetbookNotFound",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             identification = Identification.objects.create(
#                 vetbook=vetbook,
#                 chip_number=validated_data.get("chip_number"),
#                 clinic_name=validated_data.get("clinic_name"),
#                 chip_installation_location=validated_data.get("chip_installation_location"),
#                 chip_installation_date=validated_data.get("chip_installation_date"),
#             )
#             return Response(
#                 {
#                     "message": "Identification for a vetbook created successfully",
#                     "identification_id": identification.id,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
