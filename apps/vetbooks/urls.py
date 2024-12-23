from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VetbookViewSet

router = DefaultRouter()
router.register(r"vetbooks", VetbookViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Используем маршруты по умолчанию
]
