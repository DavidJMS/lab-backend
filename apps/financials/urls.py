# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandlePriceDollarView, PaymentsView

router = DefaultRouter()
router.register(r"price-dollar", HandlePriceDollarView, basename="clients")
router.register(r"payments", PaymentsView, basename="clients")

urlpatterns = [path("", include(router.urls))]
