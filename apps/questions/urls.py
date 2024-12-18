
from django.urls import path
from .views import AddQuestionAPIView

urlpatterns = [

    path('v1/create-question/', AddQuestionAPIView.as_view(), name='add_question'),  # URL для добавления вопроса


]
