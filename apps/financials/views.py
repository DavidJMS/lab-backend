# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Serializers
from apps.financials.serializers import PriceDollarModelSerializer, CreatePriceDollar

# My Models
from apps.financials.models import PriceDollar


class HandlePriceDollarView(
    viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin, viewsets.ViewSet
):

    queryset = PriceDollar.objects.all()
    serializer_class = PriceDollarModelSerializer
    permissions = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if self.action == "list":
            serializer_class = self.get_serializer_class()
        else:
            serializer_class = CreatePriceDollar
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=["get"])
    def today_tasa(self, request):
        data = PriceDollar.objects.latest()
        return Response(
            PriceDollarModelSerializer(data).data, status=status.HTTP_200_OK
        )
