# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Serializers
from apps.financials.serializers import (
    PriceDollarModelSerializer,
    CreatePriceDollar,
    CreatePaymentModelSerializer,
    PaymentModelSerializer,
    CashFlowModelSerializer,
)

# Models
from apps.financials.models import PriceDollar, Payment, CashFlow

# Filters
from django_filters.rest_framework import DjangoFilterBackend


class HandlePriceDollarView(viewsets.ModelViewSet):
    queryset = PriceDollar.objects.all()
    serializer_class = PriceDollarModelSerializer
    permissions = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action == "list":
            serializer_class = self.get_serializer_class()
        else:
            serializer_class = CreatePriceDollar
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=["get"])
    def today_tasa(self, request):
        data = PriceDollar.objects.latest()
        return Response(
            PriceDollarModelSerializer(data).data, status=status.HTTP_200_OK
        )


class PaymentsView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentModelSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"create_at": ["date", "range"]}

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action in ["create", "update"]:
            serializer_class = self.get_serializer_class()
        else:
            serializer_class = PaymentModelSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CashFlowViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["get"])
    def get_cash_flow(self, request):
        cash_flow = CashFlow.objects.filter(is_active=True)
        if cash_flow:
            data = CashFlowModelSerializer(cash_flow[0]).data
            return Response(data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"])
    def cash_flow(self, request):
        serializer = CashFlowModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
