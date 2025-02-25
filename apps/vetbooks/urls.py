from django.urls import include, path

from .views import (
    AddPhotoToVetbook,
    CreateVetbook,
    GetVetbookDetails,
    GetVetpassDetails,
)

urlpatterns = [
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
    path("v1/upload-photo/", AddPhotoToVetbook.as_view(), name="add_vetbook_photo"),
    path("v1/get-vetbook-details/<int:vetbook_id>/", GetVetbookDetails.as_view(), name="get_vetbook_details"),
    path("v1/get-vetpass-details/<int:vetbook_id>/", GetVetpassDetails.as_view(), name="get_vetpass_details"),
    path("v1/vetpass/", include("apps.vetbooks.vetpass.vetpass_urls")),
    path("v1/treatment/", include("apps.vetbooks.treatment_and_appointment.treatment_and_appointment_urls")),
]
