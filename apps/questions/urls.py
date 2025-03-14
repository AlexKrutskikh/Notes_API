from django.urls import path

from .views import AddPhotoQuestion, AddQuestion, GetAllQuestions, GetQuestionById

urlpatterns = [
    path("v1/create-question/", AddQuestion.as_view(), name="add_question"),
    path("v1/upload-photo/", AddPhotoQuestion.as_view(), name="add_question_photo"),
    path("v1/get-all-questions/", GetAllQuestions.as_view(), name="get_questions_all"),
    path("v1/get-question/<int:question_id>/", GetQuestionById.as_view(), name="get_question"),
]
