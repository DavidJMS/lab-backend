# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Serializers
from apps.medical.serializers import MedicalHistoryModelSerializer

# My Models
from apps.medical.models import MedicalHistoryClient


class HandleMedicalHistoryClientView(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = MedicalHistoryClient.objects.all()
    serializer_class = MedicalHistoryModelSerializer
    permission_classes = [AllowAny]
