from django.db import models


class PriceDollar(models.Model):

    price = models.DecimalField(max_digits=12, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ["create_at"]
        ordering = ["-create_at"]
