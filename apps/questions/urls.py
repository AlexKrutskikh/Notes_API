from django.urls import path

from .views import AddPhotoQuestion, AddQuestion

urlpatterns = [
    path("v1/create-question/", AddQuestion.as_view(), name="add_question"),
    path("v1/upload-photo/", AddPhotoQuestion.as_view(), name="add_question_photo"),
]
