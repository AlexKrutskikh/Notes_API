from django.urls import path

from .views import (
    CreateNote,
    DeleteNote,
    GetAllNotes,
    GetMyNotes,
    GetNoteById,
    RestoreNote,
    UpdateNote,
)

urlpatterns = [
    # создание заметки
    path("v1/create/note/", CreateNote.as_view(), name="CreateNote"),
    # Обновление заметки
    path("v1/update/note/", UpdateNote.as_view(), name="UpdateNote"),
    # Удаление заметки
    path("v1/delete/note/", DeleteNote.as_view(), name="DeleteNote"),
    # Восстаноление заметки
    path("v1/restore/note/", RestoreNote.as_view(), name="RestoreNote"),
    # получение всех заметок
    path("v1/get-all/notes/", GetAllNotes.as_view(), name="get_all_notes"),
    # получение своих заметок
    path("v1/get-my/note/", GetMyNotes.as_view(), name="get_my_notes"),
    # получение заметки по id
    path("v1/get-note/<int:note_id>/", GetNoteById.as_view(), name="get_note_by_id"),
]
