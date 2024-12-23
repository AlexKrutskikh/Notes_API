from django.urls import path

from .views import AddMessageView, AllMessagesView  # Импортируем функции

"""API  for saving and updating questions"""

urlpatterns = [
    path("<pk>/message/", AddMessageView().as_view(), name="add_message_to_question"),
    path("<pk>/messages/", AllMessagesView.as_view(), name="all_messages_of_question"),
]
