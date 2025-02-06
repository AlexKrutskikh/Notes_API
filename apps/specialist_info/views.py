from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from FreeVet.utils import save_files_to_storage

from ..auth.models import User
from .models import Specialist, SpecialistDocument

"""Сохранение в БД данных  специалиста"""


class CreateSpecialist(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        data = request.data

        # Проверка на наличие специалиста
        if hasattr(user, "specialist") and user.specialist is not None:
            if user.specialist.status == Specialist.SPECIALIST_VERIFICATION:
                return Response(
                    {"error": "You cannot create a specialist profile."}, status=status.HTTP_400_BAD_REQUEST
                )

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

        # Сменить статус на верификацию после заполнения
        specialist.status = Specialist.SPECIALIST_VERIFICATION
        specialist.save()

        return Response(
            {
                "message": "Specialist created successfully",
                "specialist_id": specialist.id,
            },
            status=status.HTTP_201_CREATED,
        )


"""Сохранение в БД путей к файлам и привязка к специалисту"""


class UploadSpecialistDocuments(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        specialist_id = request.data.get("specialist_id")

        try:
            specialist = Specialist.objects.get(id=specialist_id)
        except Specialist.DoesNotExist:
            return Response({"error": "Specialist not found"}, status=status.HTTP_404_NOT_FOUND)

        file_paths = save_files_to_storage(request, "specialist_documents")

        document_objects = [SpecialistDocument(path=path, user=specialist.user) for path in file_paths]

        created_objects = SpecialistDocument.objects.bulk_create(document_objects)

        # Привязка загруженных документов к специалисту
        for doc in created_objects:
            doc.specialists.add(specialist)

        # Получение идентификаторов созданных документов
        created_ids = [obj.id for obj in created_objects]

        return Response(
            {
                "message": "Documents uploaded successfully",
                "document_ids": created_ids,
            },
            status=status.HTTP_201_CREATED,
        )
