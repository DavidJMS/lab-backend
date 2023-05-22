from django.db import models
from django.utils.translation import gettext_lazy as _


class Divisa(models.TextChoices):
    Dolares = "Dolares", _("Dolares")
    Bolivares = "Bolivares", _("Bolivares")


class MethodPayment(models.TextChoices):
    Transferencia_Interbancaria = "Pago Interbancario", _("Pago Interbancario")
    Efectivo = "Efectivo", _("Efectivo")


class TypeTransaction(models.TextChoices):
    PaymentClient = "Pago del cliente", _("Pago realizado por el cliente")
    PaymentTurned = "Vuelto", _("Vuelto")
    Withdrawal = "Retiro manual", _("Retiro manual")
    Ingress = "Ingreso manual", _("Ingreso manual")


class ConcepPriceTransaction(models.TextChoices):
    Discount = "Descuento", _("Descuento en el precio final")
    Incress = "Aumento", _("Aumento en el precio final")
