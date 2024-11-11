from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import add_question, update_question, QuestionDetailView, QuestionView, AddMessageView, AllMessagesView # Импортируем функции


"""API for saving and updating questions"""

urlpatterns = [

    path('add/', add_question, name='add_question'),  # URL для добавления вопроса

    path('update/', update_question, name='update_question'),  # URL для обновления вопроса


    path('get/', QuestionDetailView.as_view(), name='question-detail'),

    path('<pk>', QuestionView.as_view(), name='question'),

    path('<pk>/message/', AddMessageView().as_view(), name='add_message_to_question'),

    path('<pk>/messages/', AllMessagesView.as_view(), name='all_messages_of_question')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
