from django.urls import path

from .views import GenerateVerificationCode, VerifySpecialist

urlpatterns = [
    path("generate-code/", GenerateVerificationCode.as_view(), name="generate-verification-code"),
    path("verify-specialist/", VerifySpecialist.as_view(), name="verify-specialist"),
]
