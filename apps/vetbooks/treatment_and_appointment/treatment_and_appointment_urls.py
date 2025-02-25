from django.urls import path

from .treatment_and_appointment_view import (
    AddFileToAppointment,
    CreateAppointment,
    CreateTreatment,
    EditAppointment,
    EditTreatment,
)

urlpatterns = [
    path("create-treatment/", CreateTreatment.as_view(), name="create_treatment"),
    path("edit-treatment/", EditTreatment.as_view(), name="edit_treatment"),
    path("create-appointment/", CreateAppointment.as_view(), name="create_appointment"),
    path("upload-file-to-appointment/", AddFileToAppointment.as_view(), name="upload_file_to_appointment"),
    path("edit-appointment/", EditAppointment.as_view(), name="edit_appointment"),
]
