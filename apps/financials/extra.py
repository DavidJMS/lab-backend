from django.db import models


class MainModel(models.Model):

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        get_latest_by = ["create_at"]
        ordering = ["-create_at"]
