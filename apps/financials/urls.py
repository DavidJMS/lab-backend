# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandlePriceDollarView

router = DefaultRouter()
router.register(r"price-dollar", HandlePriceDollarView, basename="clients")

urlpatterns = [path("", include(router.urls))]
