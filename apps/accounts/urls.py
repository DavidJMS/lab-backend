# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandleClientView, HandleAuthView

router = DefaultRouter()
router.register(r"client", HandleClientView, basename="clients")
router.register(r"auth", HandleAuthView, basename="auth")

urlpatterns = [path("", include(router.urls))]
