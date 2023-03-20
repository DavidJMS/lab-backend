# From Django Rest
from rest_framework import serializers

# Models
from .models import PriceDollar, Payment

# Serializers
from apps.medical.serializers import MedicalHistoryModelSerializer

# Formats
from django.conf import settings


class PriceDollarModelSerializer(serializers.ModelSerializer):

    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:

        model = PriceDollar
        fields = "__all__"


class CreatePriceDollar(serializers.ModelSerializer):
    class Meta:

        model = PriceDollar
        fields = "__all__"


class CreatePaymentModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = Payment
        fields = "__all__"


class PaymentModelSerializer(serializers.ModelSerializer):

    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    medical_history = MedicalHistoryModelSerializer(read_only=True)

    class Meta:

        model = Payment
        fields = "__all__"
        depth = 2
