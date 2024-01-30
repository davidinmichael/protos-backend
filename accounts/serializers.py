from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
from location.models import *
from .utils import *


class BusinessLocationSerializer(serializers.ModelSerializer):
    business = serializers.SlugRelatedField(slug_field="name", queryset=BusinessAccount.objects.all())
    class Meta:
        model = BusinessLocation
        fields = "__all__"
        read_only_fields = ["id"]


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = "__all__"
        read_only_fields = ["id"]


class PersonalAccountSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all())
    state = serializers.SlugRelatedField(
        slug_field="name", queryset=State.objects.all())
    city = serializers.SlugRelatedField(
        slug_field="name", queryset=City.objects.all())
    # location = UserLocationSerializer()

    class Meta:
        model = PersonalAccount
        fields = ["id", "first_name", "last_name", "username", "email", "country",
                  "state", "city", "user_id", "is_business_owner", "email_verified",
                  "date_joined"]

        read_only_fields = ["id"]
        write_only_fields = ["password"]

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
    
    def validate_email(self, value):
        if PersonalAccount.objects.filter(email=value).exists():
            raise ValidationError("User with this email already exist")
        return value
    
    def create(self, validated_data):
        user = PersonalAccount.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["location"] = get_location()
        return rep


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = "__all__"
        read_only_fields = ["id"]


class BusinessHourSerializer(serializers.ModelSerializer):
    business = serializers.SlugRelatedField(slug_field="name", queryset=BusinessAccount.objects.all())
    class Meta:
        model = BusinessHour
        fields = "__all__"
        read_only_fields = ["id"]


class BusinessAccountSerializer(serializers.ModelSerializer):
    owner = PersonalAccountSerializer()
    categories = BusinessCategorySerializer(many=True)
    country = serializers.SlugRelatedField(slug_field="name", queryset=Country.objects.all())
    state = serializers.SlugRelatedField(slug_field="name", queryset=State.objects.all())
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())

    class Meta:
        model = BusinessAccount
        fields = ["id", "owner", "name", "email", "contact_number", "description", "country",
                  "state", "city", "postal_code", "address", "website",
                  "business_id", "email_verified", "date_joined", "categories"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        owner = validated_data.pop("owner")
        categories = validated_data.pop("categories", None)
        hours = self.context['request'].data.get("hours")
        location = self.context["request"].data.get("location")

        business_owner = PersonalAccount.objects.create_user(**owner)
        business = BusinessAccount.objects.create(
            owner=business_owner, **validated_data)
        if categories is not None:
            for category in categories:
                cat = BusinessCategory.objects.get(name=category["name"])
                business.categories.add(cat)
        if hours is not None:
            for hour in hours:
                business_hours = BusinessHour.objects.create(
                    business=business, day=hour["day"], open_time=hour["open_time"], close_time=hour["close_time"])
        business_location = BusinessLocation.objects.create(
            business=business, latitude=location["latitude"], longitude=location["longitude"])
        return business
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        hours = instance.business_hours.all()
        location = BusinessLocation.objects.get(business=instance)
        rep["location"] = BusinessLocationSerializer(location).data
        rep["hours"] = BusinessHourSerializer(hours, many=True).data
        return rep
