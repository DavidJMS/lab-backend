from django.db import models


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

    class Meta:
        ordering = ["-create_at"]


class Payment(models.Model):

    method_payment = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo_billet = models.ImageField(upload_to="media", null=True)
    number_ref = models.CharField(max_length=30, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    medical_history = models.ForeignKey(
        MedicalHistoryClient, on_delete=models.SET_NULL, null=True, blank=False
    )
