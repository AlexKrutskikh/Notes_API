from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User
from Notes.settings import logger

from .models import Notes
from .permissions import IsOwnerOrAdminOrReadOnly

"""Создание заметки"""


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

            logger.info(f"User {request.user.username} create note")

            return Response({"message": "Successfully created", "id_note": note.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Обновление заметки"""


class UpdateNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrAdminOrReadOnly,
    )

    def post(self, request):
        note_id = request.data.get("note_id")

        try:
            note = Notes.objects.get(id=note_id)
        except Notes.DoesNotExist:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, note)

        note.title = request.data.get("title", note.title)
        note.body = request.data.get("body", note.body)
        note.updated_at = timezone.now()
        note.save()

        logger.info(f"User {request.user.username} updated note ID {note_id}")

        return Response({"message": "Successfully updated", "id_note": note.id}, status=status.HTTP_200_OK)


"""Удаление заметки"""


class DeleteNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrAdminOrReadOnly,
    )

    def post(self, request):
        note_id = request.data.get("note_id")

        if not note_id:
            return Response({"error": "Note ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            note = Notes.objects.get(id=note_id)

            self.check_object_permissions(request, note)

            if note.is_deleted:
                logger.warning(f"User {request.user.username} tried to delete an already deleted note ID {note_id}.")
                return Response({"error": "Note is already deleted."}, status=status.HTTP_400_BAD_REQUEST)

            note.is_deleted = True
            note.save()

            logger.info(f"User {request.user.username} moved note ID {note_id} to trash.")

            return Response({"message": "Successfully moved to trash", "id_note": note.id}, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            logger.error(f"Note ID {note_id} not found.")
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error deleting note ID {note_id}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Восстанволение заметки"""


class RestoreNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )

    def post(self, request):
        note_id = request.data.get("note_id")

        if not note_id:
            return Response({"error": "Note ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            note = Notes.objects.get(id=note_id)

            if not note.is_deleted:
                logger.warning(f"User {request.user.username} tried to restore a non-deleted note ID {note_id}.")
                return Response({"error": "Note is not deleted."}, status=status.HTTP_400_BAD_REQUEST)

            note.is_deleted = False
            note.save()

            logger.info(f"Admin {request.user.username} restored note ID {note_id}.")

            return Response({"message": "Successfully restored", "id_note": note.id}, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            logger.error(f"Note ID {note_id} not found.")
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error restoring note ID {note_id}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
