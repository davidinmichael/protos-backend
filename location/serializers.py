from rest_framework import serializers
from .models import *


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Country
        fields = ["name", "capital", "phone_code", "latitude", "longitude",
                  "iso2", "iso3", "flag", "currency"]
    
    def to_representation(self, instance):
        country = super().to_representation(instance)
        country["phone_code"] = f"+{country['phone_code']}"
        return country


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ["name", "latitude", "longitude", "identifier", "state_code",
                  "country"]


class CitySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(
        slug_field="name", queryset=State.objects.all())

    class Meta:
        model = City
        fields = "__all__"
