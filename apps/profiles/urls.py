from django.urls import path, include
from .views import UpdateProfileFieldsView


urlpatterns = [

    path('update/', UpdateProfileFieldsView.as_view(), name='update-profile-fields'),

]