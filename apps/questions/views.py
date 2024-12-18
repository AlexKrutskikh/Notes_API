from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QuestionFile
from .utils import save_files_to_storage
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


"""Сохранение в БД путей к файлам и привязка к пользователю по id"""

class AddPhotoQuestion(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        question_files = save_files_to_storage(request, 'question_photo', user_id)

        created_objects = QuestionFile.objects.bulk_create(question_files)

        created_ids = [obj.id for obj in created_objects]

        return Response({'ids': created_ids}, status=201)
