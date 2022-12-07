from rest_framework import serializers

from .models import Client


class ClientModelSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(read_only=True)

    class Meta:

        model = Client
        fields = "__all__"
