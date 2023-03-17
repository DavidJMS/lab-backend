# From Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits


class MedicalHistoryManager(models.Manager):
    """
    Job manager used to create a code
    """

    CODE_LENGTH = 6

    def create(self, **kwargs):
        """Handle code creation."""
        pool = ascii_uppercase + digits + ".-"
        code = kwargs.get("code", "".join(random.choices(pool, k=self.CODE_LENGTH)))
        kwargs["code"] = code
        return super(MedicalHistoryManager, self).create(**kwargs)
