from rest_framework import serializers
from accounts.serializers import BusinessAccountSerializer

from .models import *


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ["name"]
        read_only_fields = ["id"]


class BusinessProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    business = BusinessAccountSerializer()

    class Meta:
        model = BusinessProduct
        fields = "__all__"
        read_only_fields = ["id"]
