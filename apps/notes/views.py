from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from Notes.settings import logger

from .models import Notes
from .permissions import EditorReadOnly, IsOwnerOrAdminOrReadOnly

"""Создание заметки"""


class CreateNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, EditorReadOnly]

    def post(self, request):

        data = request.data

        title = data.get("title")
        body = data.get("body")
        if not title or not body:
            logger.warning(f"User {request.user.username} failed to create note: title or body is missing")
            return Response({"error": "Title and body are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            note = Notes.objects.create(
                user=request.user,
                title=title,
                body=body,
            )

            logger.info(f"User {request.user.username} created note with ID {note.id}")

            return Response(
                {"message": "Successfully created", "id_note": note.id},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            logger.error(f"Error creating note for user {request.user.username}: {str(e)}")

            return Response(
                {"error": "An error occurred while creating the note"},
                status=status.HTTP_400_BAD_REQUEST,
            )


"""Обновление заметки"""


class UpdateNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly, EditorReadOnly)

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
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly, EditorReadOnly)

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


"""Восстановление заметки"""


class RestoreNote(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (IsAuthenticated, IsAdminUser, EditorReadOnly)

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


""""Получение всех заметок"  """


class GetAllNotes(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:

            notes = Notes.objects.filter(is_deleted=False)

            notes_data = [
                {
                    "id": note.id,
                    "title": note.title,
                    "body": note.body,
                    "user_id": note.user.id,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at,
                    "is_deleted": note.is_deleted,
                }
                for note in notes
            ]
            logger.info(f"Admin {request.user.username} retrieved all notes.")
            return Response(notes_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving all notes: {str(e)}")
            return Response(
                {"error": "An error occurred while retrieving notes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


"""Получение своих заметок"""


class GetMyNotes(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            notes = Notes.objects.filter(user=request.user, is_deleted=False)

            if not notes.exists():
                logger.info(f"User {request.user.username} has no notes.")
                return Response({"message": "Notes not found"}, status=status.HTTP_200_OK)

            notes_data = [
                {
                    "id": note.id,
                    "title": note.title,
                    "body": note.body,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at,
                    "is_deleted": note.is_deleted,
                }
                for note in notes
            ]
            logger.info(f"User {request.user.username} retrieved their notes.")
            return Response(notes_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving notes for user {request.user.username}: {str(e)}")
            return Response(
                {"error": "An error occurred while retrieving notes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


"""Получение заметки по id"""


class GetNoteById(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def get(self, request, note_id):
        try:
            note = Notes.objects.get(id=note_id)

            if note.is_deleted:
                logger.warning(f"Attempt to access deleted note {note_id}.")
                return Response({"error": "This note has been deleted."}, status=status.HTTP_410_GONE)

        except Notes.DoesNotExist:
            logger.error(f"Note with ID {note_id} not found.")
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, note)

        note_data = {
            "id": note.id,
            "title": note.title,
            "body": note.body,
            "user_id": note.user.id,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "is_deleted": note.is_deleted,
        }

        logger.info(f"User {request.user.username} retrieved note ID {note_id}.")
        return Response(note_data, status=status.HTTP_200_OK)
