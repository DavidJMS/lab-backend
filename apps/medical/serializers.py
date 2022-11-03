from rest_framework import serializers

from .models import MedicalHistoryClient, MedicalExam


class MedicalExamModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalExam
        fields = "__all__"


class MedicalHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalHistoryClient
        fields = "__all__"
