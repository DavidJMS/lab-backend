# From Django
from django.db import models
from django.utils import timezone

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
        pool = digits
        code = kwargs.get("code", "".join(random.choices(pool, k=self.CODE_LENGTH)))
        kwargs["code"] = code
        kwargs["number_id"] = self.filter(create_at__date=timezone.now()).count() + 1
        return super(MedicalHistoryManager, self).create(**kwargs)
