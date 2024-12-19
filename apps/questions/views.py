from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QuestionFile, Question
from .utils import save_files_to_storage
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .serializers import QuestionSerializer
from rest_framework import status

"""Сохранение вопроса"""


class AddQuestion(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data = request.data


        serializer = QuestionSerializer(data=data)

        if serializer.is_valid():

            try:

                Question.objects.create (
                    user_id=user_id,
                    **serializer.validated_data

                )

                return Response({
                    'message': 'Successfully created',
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""Сохранение в БД путей к файлам и привязка к пользователю по id"""

class AddPhotoQuestion(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        question_files = save_files_to_storage(request, 'question_photo', user_id)

        created_objects = QuestionFile.objects.bulk_create(question_files)

        created_ids = [obj.id for obj in created_objects]

        return Response({'ids file(s)': created_ids}, status=201)
