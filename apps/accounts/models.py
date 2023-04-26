from django.db import models


class Client(models.Model):

    first_names = models.CharField(max_length=30)
    last_names = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, blank=True)
    dni = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=30)
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_names} {self.last_names}"
