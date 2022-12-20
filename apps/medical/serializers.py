from rest_framework import serializers

from .models import MedicalHistoryClient, MedicalExam, Payment
from apps.accounts.serializers import ClientModelSerializer


class MedicalExamModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalExam
        fields = "__all__"


class CreateMedicalHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalHistoryClient
        fields = "__all__"


class MedicalHistoryModelSerializer(serializers.ModelSerializer):

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

    medical_history = MedicalHistoryModelSerializer(read_only=True)

    class Meta:

        model = Payment
        fields = "__all__"
        depth = 2
