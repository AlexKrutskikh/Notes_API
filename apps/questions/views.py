from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.animals.models import Animal
from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Question, QuestionFile
from .validators import validate_question_data

"""Валидация данных вопроса"""


class AddQuestion(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Create a new question related to an animal.

        **Request Body Example:**
        ```json
        {
            "text": "What should I do if my dog refuses to eat?",
            "animal_id": 5,
            "file_ids": [1, 2, 3]
        }
        ```
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="Question text (required)"),
                "animal_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the related animal (required)"
                ),
                "file_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of uploaded file IDs (optional)",
                ),
            },
            required=["text", "animal_id"],
        ),
        responses={
            201: openapi.Response(
                "Question successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Bad Request - Validation Error",
        },
    )
    def post(self, request):

        user_id = request.user.id
        data = request.data

        try:
            validate_data = validate_question_data(data)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

        try:

            Question.objects.create(
                user=User.objects.get(id=user_id),
                text=validate_data.get("text"),
                animal=Animal.objects.get(id=validate_data.get("animal_id")),
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


"""Сохранение в БД путей к файлам и привязка к пользователю по id"""


class AddPhotoQuestion(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload photo(s) related to a question and get their IDs.",
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

            file_paths = save_files_to_storage(request, "question_photos")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        question_files = [QuestionFile(path=path, user_id=user_id) for path in file_paths]

        QuestionFile.objects.bulk_create(question_files)

        question_files_instances = QuestionFile.objects.filter(path__in=file_paths)

        created_ids = [obj.id for obj in question_files_instances]

        return Response({"message": "Successfully created", "ids file(s)": created_ids}, status=201)


"""Получение всех вопросов"""


class GetAllQuestions(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Get a list of all questions.
        """,
        responses={
            200: openapi.Response(
                "List of questions",
                openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Question ID"),
                            "text": openapi.Schema(type=openapi.TYPE_STRING, description="Question text"),
                            "animal_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Animal ID"),
                            "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                            "file_ids": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_INTEGER),
                                description="List of file IDs",
                            ),
                        },
                    ),
                ),
            ),
            401: "Unauthorized",
        },
    )
    def get(self, request):
        questions = Question.objects.all()
        result = []
        for question in questions:
            result.append(
                {
                    "id": question.id,
                    "text": question.text,
                    "animal_id": question.animal.id,
                    "user_id": question.user.id,
                    "file_ids": question.file_ids if hasattr(question, "file_ids") else [],
                }
            )
        return Response(result, status=status.HTTP_200_OK)


"""Получение вопроса по ID"""


class GetQuestionById(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Get a question by ID.
        """,
        responses={
            200: openapi.Response(
                "Question details",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Question ID"),
                        "text": openapi.Schema(type=openapi.TYPE_STRING, description="Question text"),
                        "animal_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Animal ID"),
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                        "file_ids": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description="List of file IDs",
                        ),
                    },
                ),
            ),
            404: "Not Found",
            401: "Unauthorized",
        },
    )
    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            result = {
                "id": question.id,
                "text": question.text,
                "animal_id": question.animal.id,
                "user_id": question.user.id,
                "file_ids": question.file_ids if hasattr(question, "file_ids") else [],
            }
            return Response(result, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
