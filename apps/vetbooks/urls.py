from django.urls import path

from .views import CreateVetbook

urlpatterns = [
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
]
