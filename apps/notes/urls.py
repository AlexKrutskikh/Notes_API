from django.urls import path

from .views import CreateNote, DeleteNote, UpdateNote,RestoreNote

urlpatterns = [
    # создание заметки
    path("v1/create/note/", CreateNote.as_view(), name="CreateNote"),
    # Обновление заметки
    path("v1/update/note/", UpdateNote.as_view(), name="UpdateNote"),
    # Удаление заметки
    path("v1/delete/note/", DeleteNote.as_view(), name="DeleteNote"),
    # Восстаноление заметки
    path("v1/Restore/note/", RestoreNote.as_view(), name="RestoreNote"),
]
