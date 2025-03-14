from django.urls import path

from .treatment_and_appointment_view import (
    AddFileToAppointment,
    CreateAppointment,
    CreateTreatment,
    EditAppointment,
    EditTreatment,
)
from .vetbook_views import (
    AddPhotoToVetbook,
    CreateVetbook,
    GetVetbookDetails,
    GetVetpassDetails,
)
from .vetpass_view import (
    AddFileToClinicalExamination,
    CreateClinicalExamination,
    CreateDeworming,
    CreateEctoparasiteTreatment,
    CreateIdentification,
    CreateRegistration,
    CreateVaccination,
    EditAdditionalDescription,
    EditClinicalExamination,
    EditDeworming,
    EditEctoparasiteTreatment,
    EditIdentification,
    EditRegistration,
    EditVaccination,
)

urlpatterns = [
    # vetbook_url
    path("v1/vetbook/create/", CreateVetbook.as_view(), name="create_vetbook"),
    path("v1/upload-photo/", AddPhotoToVetbook.as_view(), name="add_vetbook_photo"),
    path("v1/get-vetbook-details/<int:vetbook_id>/", GetVetbookDetails.as_view(), name="get_vetbook_details"),
    path("v1/get-vetpass-details/<int:vetbook_id>/", GetVetpassDetails.as_view(), name="get_vetpass_details"),
    # vetpass_url
    path(
        "v1/vetpass/edit-additional-description/",
        EditAdditionalDescription.as_view(),
        name="edit_additional_description",
    ),
    path("v1/vetpass/edit-identification/", EditIdentification.as_view(), name="edit_identification"),
    path("v1/vetpass/create-identification/", CreateIdentification.as_view(), name="create_identification"),
    path("v1/vetpass/edit-vaccination/", EditVaccination.as_view(), name="edit_vaccination"),
    path("v1/vetpass/create-vaccination/", CreateVaccination.as_view(), name="create_vaccination"),
    path("v1/vetpass/edit-deworming/", EditDeworming.as_view(), name="edit_deworming"),
    path("v1/vetpass/create-deworming/", CreateDeworming.as_view(), name="create_deworming"),
    path(
        "v1/vetpass/edit-ectoparasite-treatment/",
        EditEctoparasiteTreatment.as_view(),
        name="edit_ectoparasite_treatment",
    ),
    path(
        "v1/vetpass/create-ectoparasite-treatment/",
        CreateEctoparasiteTreatment.as_view(),
        name="create_ectoparasite_treatment",
    ),
    path("v1/vetpass/edit-clinical-examination/", EditClinicalExamination.as_view(), name="edit_clinical_examination"),
    path(
        "v1/vetpass/create-clinical-examination/",
        CreateClinicalExamination.as_view(),
        name="create_clinical_examination",
    ),
    path(
        "v1/vetpass/add-file-to-clinical-examination/",
        AddFileToClinicalExamination.as_view(),
        name="add_file_to_clinical_examination",
    ),
    path("v1/vetpass/edit-registration/", EditRegistration.as_view(), name="edit_registration"),
    path("v1/vetpass/create-registration/", CreateRegistration.as_view(), name="create_registration"),
    # treatment_and_appointment_view_url
    path("v1/treatment/create-treatment/", CreateTreatment.as_view(), name="create_treatment"),
    path("v1/treatment/edit-treatment/", EditTreatment.as_view(), name="edit_treatment"),
    path("v1/treatment/create-appointment/", CreateAppointment.as_view(), name="create_appointment"),
    path("v1/treatment/upload-file-to-appointment/", AddFileToAppointment.as_view(), name="upload_file_to_appointment"),
    path("v1/treatment/edit-appointment/", EditAppointment.as_view(), name="edit_appointment"),
]
