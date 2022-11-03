from django.db import models


class Client(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    dni = models.CharField(max_length=30)
    sex = models.CharField(max_length=30)
    birth_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    phone = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
