from django.urls import path
from .views import CreateNote


urlpatterns = [
    # создание заметки
    path("v1/create/note/", CreateNote.as_view(), name="CreateNote"),
]