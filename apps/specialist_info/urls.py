from django.urls import path

from .views import CreateSpecialist, UploadSpecialistDocuments

urlpatterns = [
    path("v1/specialist/create/", CreateSpecialist.as_view(), name="create_specialist"),
    path("v1/specialist/documents/", UploadSpecialistDocuments.as_view(), name="upload_specialist_documents"),
]
