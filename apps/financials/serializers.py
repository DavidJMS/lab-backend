# From Django
from django.db import transaction

# From Django Rest
from rest_framework import serializers

# Models
from .models import PriceDollar, Transaction, CashFlow, PriceTransaction

# Serializers
from apps.medical.serializers import MedicalHistoryModelSerializer

# Formats
from django.conf import settings

# Constants
from apps.financials.constants import (
    Divisa,
    MethodPayment,
    TypeTransaction,
    ConcepPriceTransaction,
)


class PriceDollarModelSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:
        model = PriceDollar
        fields = "__all__"


class CreatePriceDollar(serializers.ModelSerializer):
    class Meta:
        model = PriceDollar
        fields = "__all__"


class CreateTransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            result = super().create(validated_data)
            if result:
                total_paid = 0
                if result.medical_history:
                    if result.type == TypeTransaction.PaymentClient:
                        result.medical_history.total_paid += result.amount_dollars
                    else:
                        result.medical_history.total_paid -= result.amount_dollars
                    result.medical_history.save(update_fields=["total_paid"])
                    total_paid = result.medical_history.total_paid
                query_cash_flow = CashFlow.objects.filter(is_active=True)

                if query_cash_flow.exists():
                    cash_flow = query_cash_flow[0]
                else:
                    cash_flow = CashFlow.objects.create(
                        is_active=True,
                        amount_bolivares_cash=0.00,
                        amount_bolivares_bank=0.00,
                        amount_dollars_cash=0.00,
                        amount_dollars_bank=0.00,
                    )

                if (
                    result.divisa == Divisa.Dolares
                    and result.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_dollars_cash += result.amount_dollars
                elif (
                    result.divisa == Divisa.Bolivares
                    and result.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_bolivares_cash += result.amount_bolivares
                elif (
                    result.divisa == Divisa.Bolivares
                    and result.method_payment
                    == MethodPayment.Transferencia_Interbancaria
                ):
                    cash_flow.amount_bolivares_bank += result.amount_bolivares

                cash_flow.transactions.add(result)
                cash_flow.save()
                return result, total_paid
        raise Exception("Hubo un error guardando el pago")


class TransactionModelSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    medical_history = MedicalHistoryModelSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 2


class CashFlowModelSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:
        model = CashFlow
        fields = "__all__"
        read_only = [
            "create_at",
            "amount_bolivares_cash",
            "amount_bolivares_bank",
            "amount_dollars_cash",
            "amount_dollars_bank",
            "transactions",
        ]
        depth = 4


class PriceTransactionModelSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT, read_only=True
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price_dollar.price", read_only=True
    )

    class Meta:
        model = PriceTransaction
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            price_transaction = PriceTransaction.objects.create(**validated_data)
            price_transaction.apply_operation()
            return price_transaction, price_transaction.medical_history.total_pay
