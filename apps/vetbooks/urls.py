from django.urls import path

from .edit_vetpass_view import (
    EditAdditionalDescription,
    EditClinicalExamination,
    EditDeworming,
    EditEctoparasiteTreatment,
    EditIdentification,
    EditRegistration,
    EditVaccination,
)
from .treatment_and_appointment_view import (
    AddFileToAppointment,
    CreateAppointment,
    CreateTreatment,
    EditAppointment,
    EditTreatment,
)
from .views import AddPhotoToVetbook, CreateVetbook

urlpatterns = [
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
    path("v1/upload-photo/", AddPhotoToVetbook.as_view(), name="add_vetbook_photo"),
    path("v1/edit-additional-description/", EditAdditionalDescription.as_view(), name="edit_additional_description"),
    path("v1/edit-identification/", EditIdentification.as_view(), name="edit_identification"),
    path("v1/edit-vaccination/", EditVaccination.as_view(), name="edit_vaccination"),
    path("v1/edit-deworming/", EditDeworming.as_view(), name="edit_deworming"),
    path("v1/edit-ectoparasite-treatment/", EditEctoparasiteTreatment.as_view(), name="edit_ectoparasite_treatment"),
    path("v1/edit-clinical-examination/", EditClinicalExamination.as_view(), name="edit_clinical_examination"),
    path("v1/edit-registration/", EditRegistration.as_view(), name="edit_registration"),
    path("v1/create-treatment/", CreateTreatment.as_view(), name="create_treatment"),
    path("v1/edit-treatment/", EditTreatment.as_view(), name="edit_treatment"),
    path("v1/create-appointment/", CreateAppointment.as_view(), name="create_appointment"),
    path("v1/upload-file-to-appointment/", AddFileToAppointment.as_view(), name="upload_file_to_appointment"),
    path("v1/edit-appointment/", EditAppointment.as_view(), name="edit_appointment"),
]
