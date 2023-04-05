from django.db import models
from django.utils.translation import gettext_lazy as _


class Divisa(models.TextChoices):
    Dolares = "Dolares", _("Dolares")
    Bolivares = "Bolivares", _("Bolivares")


class MethodPayment(models.TextChoices):
    Transferencia_Interbancaria = "Pago Interbancario", _("Pago Interbancario")
    Efectivo = "Efectivo", _("Efectivo")


class TypePayment(models.TextChoices):
    PaymentClient = "PaymentClient", _("Payment Client to pay exams")
    PaymentTurned = "PaymentTurned", _("Payment Turned by employee")
