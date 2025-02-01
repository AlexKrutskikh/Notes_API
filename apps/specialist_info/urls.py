from django.urls import path

from .views import AddSpecialist

urlpatterns = [
    path("v1/specialist/create/", AddSpecialist.as_view(), name="specialist-create"),
]
