from django.urls import path

from .views import AddPhotoToVetbook, CreateVetbook, EditAdditionalDescription

urlpatterns = [
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
    path("v1/upload-photo/", AddPhotoToVetbook.as_view(), name="add_vetbook_photo"),
    path("v1/edit-additional-description/", EditAdditionalDescription.as_view(), name="edit_additional_description"),
]
