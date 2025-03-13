from django.urls import path

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
    path("edit-additional-description/", EditAdditionalDescription.as_view(), name="edit_additional_description"),
    path("edit-identification/", EditIdentification.as_view(), name="edit_identification"),
    path("create-identification/", CreateIdentification.as_view(), name="create_identification"),
    path("edit-vaccination/", EditVaccination.as_view(), name="edit_vaccination"),
    path("create-vaccination/", CreateVaccination.as_view(), name="create_vaccination"),
    path("edit-deworming/", EditDeworming.as_view(), name="edit_deworming"),
    path("create-deworming/", CreateDeworming.as_view(), name="create_deworming"),
    path("edit-ectoparasite-treatment/", EditEctoparasiteTreatment.as_view(), name="edit_ectoparasite_treatment"),
    path("create-ectoparasite-treatment/", CreateEctoparasiteTreatment.as_view(), name="create_ectoparasite_treatment"),
    path("edit-clinical-examination/", EditClinicalExamination.as_view(), name="edit_clinical_examination"),
    path("create-clinical-examination/", CreateClinicalExamination.as_view(), name="create_clinical_examination"),
    path(
        "add-file-to-clinical-examination/",
        AddFileToClinicalExamination.as_view(),
        name="add_file_to_clinical_examination",
    ),
    path("edit-registration/", EditRegistration.as_view(), name="edit_registration"),
    path("create-registration/", CreateRegistration.as_view(), name="create_registration"),
]
