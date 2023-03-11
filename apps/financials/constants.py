from django.db import models
from django.utils.translation import gettext_lazy as _


class Divisa(models.TextChoices):
    Dolares = "Dolares", _("Dolares")
    Bolivares = "Bolivares", _("Bolivares")


class MethodPayment(models.TextChoices):
    Transferencia_Interbancaria = "Transferencia Interbancaria", _(
        "Transferencia Interbancaria"
    )
    Efectivo = "Efectivo", _("Efectivo")
