from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Specialist, SpecialistDocument

"""Загрузка документов специалиста """


class UploadSpecialistDocuments(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id

        try:
            file_paths = save_files_to_storage(request, "specialist_documents")
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Создание документов в базе данных
        document_objects = [SpecialistDocument(path=path, user_id=user_id) for path in file_paths]
        created_objects = SpecialistDocument.objects.bulk_create(document_objects)

        created_ids = [obj.id for obj in created_objects]

        return Response(
            {
                "message": "Documents uploaded successfully",
                "document_ids": created_ids,
            },
            status=status.HTTP_201_CREATED,
        )


"""Создание специалиста и привязка документов """


class CreateSpecialist(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        data = request.data

        document_ids = data.get("document_ids", [])

        # Проверка статуса перед созданием специалиста
        if user.status != "Specialist_info_fill":
            return Response({"error": "Unable to create a specialist profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание нового специалиста
        specialist = Specialist.objects.create(
            user=user,
            name=data.get("name"),
            last_name=data.get("last_name"),
            specialization=data.get("specialization"),
            animals=data.get("animals"),
            telegram=data.get("telegram"),
            additional_info=data.get("additional_info", ""),
        )

        # Привязка документов к специалисту
        documents = SpecialistDocument.objects.filter(id__in=document_ids)

        if not documents:
            return Response({"error": "No valid documents found."}, status=status.HTTP_400_BAD_REQUEST)

        for doc in documents:
            doc.specialist = specialist
            doc.save()

        # Обновление статуса пользователя
        user.status = "Specialist_verification"
        user.save()

        return Response(
            {
                "message": "Specialist created successfully",
                "specialist_id": specialist.id,
                "linked_documents": [doc.id for doc in documents],
            },
            status=status.HTTP_201_CREATED,
        )
