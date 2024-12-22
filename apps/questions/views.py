from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QuestionFile, Question
from .utils import save_files_to_storage
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import status
from apps.animals.models import  Animal
from apps.auth.models import User
from .validators import validate_question_data

"""Валидация данных вопроса"""

class AddQuestion(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data=request.data

        try:
            validate_data = validate_question_data(data)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


        try:

            Question.objects.create (

                user=User.objects.get(id=user_id),
                text=validate_data.get('text'),
                animal = Animal.objects.get(id=validate_data.get('animal_id')),
                file_ids = validate_data.get('file_ids')

                        )


            return Response({
                'message': 'Successfully created',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



"""Сохранение в БД путей к файлам и привязка к пользователю по id"""

class AddPhotoQuestion(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        try:

            question_files = save_files_to_storage(request, 'question_photo', user_id)

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



        created_objects = QuestionFile.objects.bulk_create(question_files)

        created_ids = [obj.id for obj in created_objects]

        return Response({'message': 'Successfully created',
                         'ids file(s)': created_ids}, status=201)
