from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Specialist, SpecialistDocument

"""Сохранение в БД данных  специалиста"""


class CreateSpecialist(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        try:

            specialist = Specialist.objects.create(
                user=user,
                name=data.get("name"),
                last_name=data.get("last_name"),
                specialization=data.get("specialization"),
                animals=data.get("animals"),
                telegram=data.get("telegram"),
                additional_info=data.get("additional_info", ""),
            )

            return Response(
                {
                    "message": "Specialist created successfully",
                    "specialist_id": specialist.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Сохранение в БД путей к файлам и привязка к специалисту"""


class UploadSpecialistDocuments(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, specialist_id):
        try:
            specialist = Specialist.objects.get(id=specialist_id)
        except Specialist.DoesNotExist:
            return Response({"error": "Specialist not found"}, status=status.HTTP_404_NOT_FOUND)

        try:

            file_paths = save_files_to_storage(request, "specialist_documents")

            document_objects = [SpecialistDocument(path=path, user=specialist.user) for path in file_paths]

            created_objects = SpecialistDocument.objects.bulk_create(document_objects)

            for doc in created_objects:
                doc.specialists.add(specialist)

            created_ids = [obj.id for obj in created_objects]

            return Response(
                {
                    "message": "Documents uploaded successfully",
                    "document_ids": created_ids,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
