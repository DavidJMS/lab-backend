# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandleClientView

router = DefaultRouter()
router.register(r"", HandleClientView, basename="clients")

urlpatterns = [path("", include(router.urls))]
