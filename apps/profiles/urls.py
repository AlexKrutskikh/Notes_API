from django.urls import path
from .views import ChangeAvatareProfile, EditProfile

urlpatterns = [
    path("v1/profile/change-avatar/", ChangeAvatareProfile.as_view(), name="profile-change-avatar"),

    path("v1/profile/edit-profile/", EditProfile.as_view(), name="edit-profile"),

]
