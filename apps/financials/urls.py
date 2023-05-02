# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import HandlePriceDollarView, TransactionsView, CashFlowViewSet

router = DefaultRouter()
router.register(r"price-dollar", HandlePriceDollarView, basename="price-dollar")
router.register(r"transactions", TransactionsView, basename="transactions")
router.register(r"cash-flow", CashFlowViewSet, basename="cash-flow")

urlpatterns = [path("", include(router.urls))]
