# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandlePriceDollarView, PaymentsView, CashFlowViewSet

router = DefaultRouter()
router.register(r"price-dollar", HandlePriceDollarView, basename="price-dollar")
router.register(r"payments", PaymentsView, basename="payments")
router.register(r"", CashFlowViewSet, basename="cash-flow")

urlpatterns = [path("", include(router.urls))]
