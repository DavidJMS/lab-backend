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
    ResultExamClientModelSerializer,
    ResultExamClientByCode,
)
from apps.accounts.serializers import ClientModelSerializer
from apps.financials.serializers import PaymentModelSerializer

# My Models
from apps.medical.models import MedicalHistoryClient, MedicalExam, ResultExamClient
from apps.accounts.models import Client
from apps.financials.models import Payment


class HandleMedicalExamView(viewsets.ModelViewSet):
    queryset = MedicalExam.objects.all()
    serializer_class = MedicalExamModelSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"name": ["icontains"]}


class HandleResultsView(viewsets.ModelViewSet):
    queryset = ResultExamClient.objects.all()
    serializer_class = ResultExamClientModelSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action == "get_results_by_code":
            serializer_class = ResultExamClientByCode
        else:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=["post"])
    def get_results_by_code(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results, medical_history = serializer.get()
        data = {"results": results, "medical_history": medical_history}
        return Response(data, status=status.HTTP_200_OK)


class HandleMedicalHistoryClientView(viewsets.ModelViewSet):
    serializer_class = CreateMedicalHistoryModelSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "create_at": ["date"],
        "client__dni": ["exact"],
        "number_id": ["exact"],
        "with_samples": ["exact"],
    }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action == "get_payments":
            serializer_class = PaymentModelSerializer
        elif self.action == "get_results":
            serializer_class = ResultExamClientModelSerializer
        elif self.action not in ["create", "update"]:
            serializer_class = MedicalHistoryModelSerializer
        elif self.action in ["create", "update"]:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        if self.action == "get_payments":
            return Payment.objects.filter(medical_history__pk=self.medical_history_pk)
        elif self.action == "get_results":
            return ResultExamClient.objects.filter(
                medical_history__pk=self.medical_history_pk
            )
        return MedicalHistoryClient.objects.all()

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
        data["client"] = client.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["get"])
    def get_payments(self, request, *args, **kwargs):
        self.medical_history_pk = kwargs.get("pk")
        queryset = self.get_queryset()
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_results(self, request, *args, **kwargs):
        self.medical_history_pk = kwargs.get("pk")
        queryset = self.get_queryset()
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)
