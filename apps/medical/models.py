from django.db import models

from apps.financials.models import PriceDollar


class MedicalExam(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=12, decimal_places=2)


class ResultExamClient(models.Model):

    name = models.CharField(max_length=50)
    document = models.FileField(upload_to="media")


class MedicalHistoryClient(models.Model):

    client = models.ForeignKey("accounts.Client", on_delete=models.SET_NULL, null=True)
    medical_exams = models.ManyToManyField(MedicalExam)
    results_exams = models.ManyToManyField(ResultExamClient, blank=True)
    total_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_pay_bs():
        prioe_dollar = PriceDollar.objects.latest("price")
        if prioe_dollar:
            return total_pay * prioe_dollar.price
        return "No se encontro una tasa que refleje el precio del dollar en bolivares"

    class Meta:
        ordering = ["-create_at"]
