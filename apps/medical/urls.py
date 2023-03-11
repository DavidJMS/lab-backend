# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandleMedicalHistoryClientView, HandleMedicalExamView

router = DefaultRouter()
router.register(
    r"history-client",
    HandleMedicalHistoryClientView,
    basename="medical-history-client",
)
router.register(
    r"exams",
    HandleMedicalExamView,
    basename="exams",
)
urlpatterns = [path("", include(router.urls))]
