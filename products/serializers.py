from rest_framework import serializers
from accounts.serializers import BusinessAccountSerializer, PersonalAccountSerializer

from .models import *


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ["name"]
        read_only_fields = ["id"]


class BusinessProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name",
                                            queryset=ProductCategory.objects.all())
    business = serializers.SlugRelatedField(slug_field="name",
                                            queryset=BusinessAccount.objects.all())
    owner = serializers.SlugRelatedField(slug_field="name",
                                            queryset=PersonalAccount.objects.all())

    class Meta:
        model = BusinessProduct
        fields = "__all__"
        read_only_fields = ["id"]


class BusinessProductGetSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    business = BusinessAccountSerializer()
    owner = PersonalAccountSerializer()
    class Meta:
        model = BusinessProduct
        fields = "__all__"
        read_only_fields = ["id"]
