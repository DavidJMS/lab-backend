from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Client


class ClientModelSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(read_only=True)

    class Meta:

        model = Client
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.

    Handle the login request data.
    """

    username = serializers.CharField(min_length=4, max_length=60)
    password = serializers.CharField(min_length=4, max_length=16)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"general": "Credenciales Inválidas"})
        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])
        # task.test_celery.delay() # Quit after test server celery!
        return self.context["user"], token.key
