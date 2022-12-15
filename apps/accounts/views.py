# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Serializers
from apps.accounts import serializers

# My Models
from apps.accounts.models import Client


class HandleClientView(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["dni"]

    queryset = Client.objects.all()
    serializer_class = serializers.ClientModelSerializer
    permissions = [AllowAny]
