from rest_framework import serializers

from .models import MedicalHistoryClient, MedicalExam, Payment
from apps.accounts.serializers import ClientModelSerializer

# Formats
from django.conf import settings


class MedicalExamModelSerializer(serializers.ModelSerializer):
    create_at = serializers.DateField(format=settings.DATETIME_FORMAT)

    class Meta:

        model = MedicalExam
        fields = "__all__"


class CreateMedicalHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalHistoryClient
        fields = "__all__"


class MedicalHistoryModelSerializer(serializers.ModelSerializer):

    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    client = ClientModelSerializer()

    class Meta:

        model = MedicalHistoryClient
        fields = "__all__"
        depth = 2


class CreatePaymentModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = Payment
        fields = "__all__"


class PaymentModelSerializer(serializers.ModelSerializer):

    payment_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    medical_history = MedicalHistoryModelSerializer(read_only=True)

    class Meta:

        model = Payment
        fields = "__all__"
        depth = 2
