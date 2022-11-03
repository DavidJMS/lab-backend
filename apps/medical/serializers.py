from rest_framework import serializers

from .models import MedicalHistoryClient


class MedicalHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = MedicalHistoryClient
        fields = "__all__"
