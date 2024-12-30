from django.urls import path
from .views import ChangeAvatareProfile, EditProfile, UpdatePerks

urlpatterns = [
    path("v1/profile/change-avatar/", ChangeAvatareProfile.as_view(), name="change-avatar"),

    path("v1/profile/edit-profile/", EditProfile.as_view(), name="edit-profile"),

    path("v1/profile/update-perks/", UpdatePerks.as_view(), name="update-perks"),

]
