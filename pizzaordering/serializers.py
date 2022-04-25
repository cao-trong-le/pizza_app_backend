from rest_framework import serializers
from .models import (
    Product, Base, Order, Receipt, SecretKeys
)
from rest_framework.serializers import ValidationError
from rest_framework.serializers import (
    ValidationError,
    SerializerMethodField,
    HyperlinkedModelSerializer
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
        
class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = "__all__"


class SecretKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretKeys
        fields = "__all__"
