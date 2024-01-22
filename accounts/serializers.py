from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
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

    def validate_country(self, value):
        return Country.objects.get(name=value)

    def validate_state(self, value):
        return State.objects.get(name=value)

    def validate_city(self, value):
        return City.objects.get(name=value)
    
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValidationError(
                "Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError(
                "Password must contain at least one special character")
        return value


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = "__all__"
        read_only_fields = ["id"]


class BusinessAccountSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessAccount
        fields = "__all__"
        read_only_fields = ["id"]

class BusinessHourSerializer(serializers.ModelSerializer):
    business = BusinessAccountSerializer()
    class Meta:
        model = BusinessHour
        fields = "__all__"
        read_only_fields = ["id"]


# class BusinessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusinessAccount
#         fields = ""
