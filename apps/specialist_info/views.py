from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Specialist, SpecialistDocument
from .validators import validate_specialist_data

"""Загрузка документов специалиста """


class UploadSpecialistDocuments(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload file(s) related to a specialist and get their IDs.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "photos": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, format="binary"),
                    description="List of image files to upload",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                "Files successfully uploaded",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "ids file(s)": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description="List of uploaded file IDs",
                        ),
                    },
                ),
            ),
            400: "Bad Request - File Upload Error",
        },
    )
    def post(self, request):
        user_id = request.user.id

        try:
            file_paths = save_files_to_storage(request, "specialist_documents")
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        specialist_documents = [SpecialistDocument(path=path, user_id=user_id) for path in file_paths]
        SpecialistDocument.objects.bulk_create(specialist_documents)

        specialist_documents_instances = SpecialistDocument.objects.filter(path__in=file_paths)
        created_ids = [obj.id for obj in specialist_documents_instances]
        return Response({"message": "Successfully created", "ids file(s)": created_ids}, status=201)


"""Создание специалиста и привязка документов """


class CreateSpecialist(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
            Create a new Specialist.

            **Request Body Example:**
            ```json
            {
                "name": "олег",
                "last_name": "Петров",
                "specialization": "Ветеринар",
                "animals": ["Собаки", "Кошки"],
                "telegram": "@ivan_petrov",
                "additional_info": "Работаю с экзотическими животными.",
                "file_ids": [1,2,3]
            }
            ```
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Имя специалиста (обязательное)"),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Фамилия специалиста (обязательное)"),
                "specialization": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Специализация специалиста (обязательное)"
                ),
                "animals": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="Список животных, с которыми работает специалист (обязательное)",
                ),
                "telegram": openapi.Schema(type=openapi.TYPE_STRING, description="Контакт в Telegram (необязательное)"),
                "additional_info": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Дополнительная информация (необязательное)"
                ),
                "file_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список идентификаторов загруженных файлов (необязательное)",
                ),
            },
            required=["name", "last_name", "specialization", "animals"],
        ),
        responses={
            201: openapi.Response(
                "Specialist successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID созданного специалиста"),
                    },
                ),
            ),
            400: "Bad Request - Validation Error",
        },
    )
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        data = request.data

        # Проверка статуса перед созданием специалиста
        if user.status != "Specialist_info_fill":
            return Response({"error": "Unable to create a specialist profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Валидация данных
        try:
            validate_data = validate_specialist_data(data)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

        try:

            if Specialist.objects.filter(user=user).exists():
                raise ValidationError("Специалист для данного пользователя уже существует.")

            # Создание нового специалиста
            Specialist.objects.create(
                user=user,
                name=validate_data.get("name"),
                last_name=validate_data.get("last_name"),
                specialization=validate_data.get("specialization"),
                animals=validate_data.get("animals"),
                telegram=validate_data.get("telegram"),
                additional_info=validate_data.get("additional_info", ""),
                file_ids=validate_data.get("file_ids"),
            )

            return Response(
                {
                    "message": "Successfully created",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
