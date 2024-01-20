from rest_framework import serializers
from .models import BusinessAccount, BusinessCategory, PersonalAccount
from location.models import *


class PersonalAccountSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all())
    state = serializers.SlugRelatedField(
        slug_field="name", queryset=State.objects.all())
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=City.objects.all())

    class Meta:
        model = PersonalAccount
        fields = "__all__"

        read_only_fields = ["id"]
        write_only_fields = ["password"]


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = "__all__"
        read_only_fields = ["id"]

class BusinessAccountSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        queryset=BusinessAccount.objects.all(), slug_field="owner")

    class Meta:
        model = BusinessAccount
        fields = "__all__"
        read_only_fields = ["id"]
