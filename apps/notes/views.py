from .models import Notes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User


class CreateNote(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data = request.data

        try:

            note = Notes.objects.create(
                user=User.objects.get(id=user_id),
                title=data.get("title"),
                body=data.get("body"),
            )

            return Response({"message": "Successfully created", "id_note": note.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
