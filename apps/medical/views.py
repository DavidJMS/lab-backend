# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Serializers
from apps.medical.serializers import (
    CreateMedicalHistoryModelSerializer,
    MedicalHistoryModelSerializer,
    MedicalExamModelSerializer,
)
from apps.accounts.serializers import ClientModelSerializer

# My Models
from apps.medical.models import MedicalHistoryClient, MedicalExam
from apps.accounts.models import Client


class HandleMedicalExamView(viewsets.ModelViewSet):

    queryset = MedicalExam.objects.all()
    serializer_class = MedicalExamModelSerializer
    permission_classes = [AllowAny]


class HandleMedicalHistoryClientView(viewsets.ModelViewSet):

    queryset = MedicalHistoryClient.objects.all()
    serializer_class = CreateMedicalHistoryModelSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"create_at": ["date"], "client__dni": ["exact"]}

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action not in ["create", "update"]:
            serializer_class = MedicalHistoryModelSerializer
        else:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            dni: str = data["dni"]
        except AttributeError as e:
            return Response({message: "El dni es requerido"})
        clients = Client.objects.filter(dni=dni)
        client = False
        if not clients.exists():
            serializer = ClientModelSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            client = serializer.save()
        else:
            client = clients[0]
            print("sss", client)
        data["client"] = client.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
