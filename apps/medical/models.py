# Django
from django.db import models

# My Models
from apps.financials.models import PriceDollar

# My Managers
from apps.medical.managers import MedicalHistoryManager


# My Constants
from apps.medical.constants import TypeMedical


class MedicalExam(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)


class MedicalHistoryClient(models.Model):
    client = models.ForeignKey("accounts.Client", on_delete=models.SET_NULL, null=True)
    medical_exams = models.ManyToManyField(MedicalExam)
    total_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    create_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
    number_id = models.IntegerField(null=True)
    type = models.CharField(
        max_length=30, choices=TypeMedical.choices, default=TypeMedical.Particular
    )

    deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    with_samples = models.BooleanField(default=False)
    result_sent = models.BooleanField(default=False)

    @property
    def total_pay_bs():
        prioe_dollar = PriceDollar.objects.latest("price")
        if prioe_dollar:
            return total_pay * prioe_dollar.price
        return "No se encontro una tasa que refleje el precio del dolar en bolivares"

    objects = MedicalHistoryManager()

    class Meta:
        ordering = ["-create_at"]


class ResultExamClient(models.Model):
    medical_history = models.ForeignKey(
        MedicalHistoryClient, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to="results")

    def delete_document(self, path: str):
        import os

        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def delete(self, *args, **kwargs):
        if self.document:
            self.delete_document(self.document.path)
        super().delete(*args, **kwargs)
