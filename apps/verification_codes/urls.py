from django.urls import path

from .views import UpdateVerifyCodeView, VerifyCodeVetView

urlpatterns = [
    path("update_verify_code/", UpdateVerifyCodeView.as_view(), name="Update_VerifyCode"),
    path("verify_code_vet/", VerifyCodeVetView.as_view(), name="verify_code_vet"),
]
