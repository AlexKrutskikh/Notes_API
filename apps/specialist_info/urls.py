from django.urls import path

from .views import SpecialistCreateAPIView

urlpatterns = [
    path("v1/specialist/create/", SpecialistCreateAPIView.as_view(), name="specialist-create"),
]
