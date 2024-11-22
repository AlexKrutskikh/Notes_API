from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import add_question, update_question, QuestionView, AddMessageView, AllMessagesView, \
    AllQuestionsByUser, BookQuestionView  # Импортируем функции


"""API  for saving and updating questions"""

urlpatterns = [


    path('<pk>/message/', AddMessageView().as_view(), name='add_message_to_question'),

    path('<pk>/messages/', AllMessagesView.as_view(), name='all_messages_of_question')

]