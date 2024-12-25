from django.urls import path

from .views import UpdateProfileFieldsView

urlpatterns = [
    path("update/", UpdateProfileFieldsView.as_view(), name="update-profile-fields"),
]
