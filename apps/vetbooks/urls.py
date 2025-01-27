from django.urls import path

from .views import AddIdentification, CreateVetbook, VetbookInfo

urlpatterns = [
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
    path("/v1/vetbooks/get_info/", VetbookInfo.as_view(), name="get_vetbook"),
    path("v1/vetbook/add_identification/", AddIdentification.as_view(), name="add_identification"),
]
