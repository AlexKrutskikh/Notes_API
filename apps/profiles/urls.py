from django.urls import path
from .views import ChangeAvatareProfile

urlpatterns = [
    path("v1/profile/change-avatar/", ChangeAvatareProfile.as_view(), name="profile-change-avatar"),
]
