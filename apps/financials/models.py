# From Django
from django.db import models
from .extra import MainModel


# My Imports
from apps.financials.constants import Divisa, MethodPayment, TypePayment


class PriceDollar(MainModel):
    price = models.DecimalField(max_digits=12, decimal_places=2)


class Payment(MainModel):
    # Main Data
    price = models.ForeignKey(
        PriceDollar, on_delete=models.SET_NULL, null=True, blank=False
    )
    divisa = models.CharField(max_length=50, choices=Divisa.choices)
    method_payment = models.CharField(max_length=50, choices=MethodPayment.choices)
    amount_bolivares = models.DecimalField(max_digits=10, decimal_places=2)
    amount_dollars = models.DecimalField(max_digits=10, decimal_places=2)
    medical_history = models.ForeignKey(
        "medical.MedicalHistoryClient",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    # Ref Data
    number_ref = models.CharField(max_length=30, null=True, blank=True)
    photo_billet = models.ImageField(upload_to="media", null=True, blank=True)
    type = models.CharField(max_length=50, choices=TypePayment.choices)


class CashFlow(MainModel):
    is_active = models.BooleanField(default=True)
    amount_bolivares_cash = models.DecimalField(max_digits=10, decimal_places=2)
    amount_bolivares_bank = models.DecimalField(max_digits=10, decimal_places=2)
    amount_dollars_cash = models.DecimalField(max_digits=10, decimal_places=2)
    amount_dollars_bank = models.DecimalField(max_digits=10, decimal_places=2)
    transactions = models.ManyToManyField(to=Payment)

    class Meta:
        ordering = ["-id"]
