# From Django
from django.db import models
from django.db.transaction import atomic

# Utils
from .extra import MainModel
import decimal

# My Imports
from apps.financials.constants import (
    Divisa,
    MethodPayment,
    TypeTransaction,
    ConcepPriceTransaction,
)


class PriceDollar(MainModel):
    price = models.DecimalField(max_digits=12, decimal_places=2)


class Transaction(MainModel):
    # Main Data
    amount = models.ForeignKey(
        PriceDollar, on_delete=models.SET_NULL, null=True, blank=False
    )
    divisa = models.CharField(max_length=50, choices=Divisa.choices)
    method_payment = models.CharField(max_length=50, choices=MethodPayment.choices)
    amount_bolivares = models.DecimalField(max_digits=10, decimal_places=2)
    amount_dollars = models.DecimalField(max_digits=10, decimal_places=2)
    medical_history = models.ForeignKey(
        "medical.MedicalHistoryClient",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    # Ref Data
    number_ref = models.CharField(max_length=30, null=True, blank=True)
    photo_billet = models.ImageField(upload_to="media", null=True, blank=True)
    type = models.CharField(max_length=50, choices=TypeTransaction.choices)

    def delete(self, *args, **kwargs):
        total_paid = 0
        query_cash_flow = self.cashflow_set.all()
        if query_cash_flow.exists():
            cash_flow = query_cash_flow[0]
            if self.type == TypeTransaction.PaymentClient:
                self.medical_history.total_paid -= self.amount_dollars
                self.medical_history.save(update_fields=["total_paid"])
                total_paid = self.medical_history.total_paid
                if (
                    self.divisa == Divisa.Dolares
                    and self.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_dollars_cash -= self.amount_dollars
                elif (
                    self.divisa == Divisa.Bolivares
                    and self.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_bolivares_cash -= self.amount_bolivares
                elif (
                    self.divisa == Divisa.Bolivares
                    and self.method_payment == MethodPayment.Transferencia_Interbancaria
                ):
                    cash_flow.amount_bolivares_bank -= self.amount_bolivares
            elif self.type == TypeTransaction.PaymentTurned:
                self.medical_history.total_paid += self.amount_dollars
                self.medical_history.save(update_fields=["total_paid"])
                total_paid = self.medical_history.total_paid
                if (
                    self.divisa == Divisa.Dolares
                    and self.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_dollars_cash += self.amount_dollars
                elif (
                    self.divisa == Divisa.Bolivares
                    and self.method_payment == MethodPayment.Efectivo
                ):
                    cash_flow.amount_bolivares_cash += self.amount_bolivares
                elif (
                    self.divisa == Divisa.Bolivares
                    and self.method_payment == MethodPayment.Transferencia_Interbancaria
                ):
                    cash_flow.amount_bolivares_bank += self.amount_bolivares
            cash_flow.transactions.remove(self)
            cash_flow.save()
        super().delete(*args, **kwargs)
        return total_paid


class PriceTransaction(MainModel):
    """
    Esta clase contiene guarda los descuentos y aumentos de precios
    hacia un MedicalHistory
    """

    price_dollar = models.ForeignKey(
        PriceDollar, on_delete=models.SET_NULL, null=True, blank=False
    )
    amount_bolivares = models.DecimalField(max_digits=10, decimal_places=2)
    amount_dollars = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.CharField(max_length=10, choices=ConcepPriceTransaction.choices)
    medical_history = models.ForeignKey(
        "medical.MedicalHistoryClient",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    class Meta:
        ordering = ["-id"]

    def reverse_apply_operation(self):
        match (self.concept):
            case ConcepPriceTransaction.Discount:
                self.medical_history.total_pay += self.amount_dollars
            case ConcepPriceTransaction.Incress:
                self.medical_history.total_pay -= self.amount_dollars
        self.medical_history.save(update_fields=["total_pay"])
        return self.medical_history.total_pay

    def apply_operation(self):
        match (self.concept):
            case ConcepPriceTransaction.Discount:
                self.medical_history.total_pay -= self.amount_dollars
            case ConcepPriceTransaction.Incress:
                self.medical_history.total_pay += self.amount_dollars
        self.medical_history.save(update_fields=["total_pay"])

    def delete(self):
        with atomic():
            total = self.reverse_apply_operation()
            super().delete()
            return total


class CashFlow(MainModel):
    is_active = models.BooleanField(default=True)
    amount_bolivares_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    amount_bolivares_bank = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    amount_dollars_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    amount_dollars_bank = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    transactions = models.ManyToManyField(to=Transaction)

    class Meta:
        ordering = ["-id"]
