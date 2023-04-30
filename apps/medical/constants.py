from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeMedical(models.TextChoices):
    Particular = "Particular", _("El cliente lo hace por cuenta propia")
    Hospitalizado = "Hospitalizado", _("El cliente lo hace porque esta hospitalizado")
