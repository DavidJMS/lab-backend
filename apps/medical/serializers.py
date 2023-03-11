from rest_framework import serializers

from .models import MedicalHistoryClient, MedicalExam
from apps.accounts.serializers import ClientModelSerializer

# Formats
from django.conf import settings


class MedicalExamModelSerializer(serializers.ModelSerializer):
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
