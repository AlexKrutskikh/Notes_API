from django.urls import path, include
from .views import  AddAnimalAPIView

urlpatterns = [

path('v1/create/animal/', AddAnimalAPIView.as_view(), name='AddAnimalAPIView'),

]