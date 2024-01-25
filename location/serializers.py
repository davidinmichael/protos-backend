from rest_framework import serializers
from .models import *


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    # currency = serializers.SlugRelatedField(
    #     slug_field="name", queryset=Currency.objects.all())
    currency = CurrencySerializer()

    class Meta:
        model = Country
        fields = "__all__"
    
    def to_representation(self, instance):
        country = super().to_representation(instance)
        country["phone_code"] = f"+{country['phone_code']}"
        return country


class StateSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all())

    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(
        slug_field="name", queryset=State.objects.all())

    class Meta:
        model = City
        fields = "__all__"
