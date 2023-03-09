from rest_framework import serializers
from .models import PriceDollar

# Formats
from django.conf import settings


class PriceDollarModelSerializer(serializers.ModelSerializer):

    create_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    class Meta:

        model = PriceDollar
        fields = "__all__"


class CreatePriceDollar(serializers.ModelSerializer):
    class Meta:

        model = PriceDollar
        fields = "__all__"
