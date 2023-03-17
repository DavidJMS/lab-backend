from rest_framework import serializers

from .models import MedicalHistoryClient, MedicalExam, ResultExamClient
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


class ResultExamClientModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = ResultExamClient
        fields = "__all__"


class ResultExamClientByCode(serializers.Serializer):

    id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            self.result = MedicalHistoryClient.objects.get(id=data["id"])
            if self.result.code != data["code"]:
                raise serializers.ValidationError("Código inválido")
            self.id = data["id"]
        except ResultExamClient.DoesNotExist:
            raise serializers.ValidationError("Link inválido")
        return data

    def get(self):
        query = ResultExamClient.objects.filter(medical_history__id=self.id)
        results = ResultExamClientModelSerializer(query, many=True).data
        medical_history = MedicalHistoryModelSerializer(self.result).data
        return results, medical_history
