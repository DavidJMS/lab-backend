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
    filterset_fields = {
        "dni": ["iexact"],
        "first_names": ["icontains"],
        "last_names": ["icontains"],
    }

    queryset = Client.objects.all()
    serializer_class = serializers.ClientModelSerializer
    permissions = [AllowAny]


class HandleAuthView(viewsets.GenericViewSet):
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        return Response(
            {
                "message": "Login realizado con exito",
                "user": user.username,
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        user = request.user
        user.last_login = datetime_modules.datetime.now()
        user.save()
        user.auth_token.delete()
        data = {"message": "Te haz desconectado del sistema"}
        return Response(data, status=status.HTTP_200_OK)
