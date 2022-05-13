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
        fields = [
            "product_name",
            "product_description",
            "product_group",
            "product_type",
            "product_price", 
            "product_size",
            "product_discount",
            "product_note",
            "product_is_sample"
        ]
        
    def validate(self, data):
        print("[validate]: inside validate")
        print(data)
        
        # initial data
        # initial_data = self.initial_data
        # print(initial_data)
        
        # save images
        
        
        return data

    def create(self, validated_data):
        # initial data
        initial_data = self.initial_data
        print(initial_data)
        
        # save validated data
        instance = self.Meta.model(**validated_data)
        
        # save images
        image = initial_data.get("product_image", None)
        
        if image != "null":
            instance.base_image = image
        instance.save()
        
        return instance
    
        # pass
        
        
class BaseSerializer(serializers.ModelSerializer):
    base_name = serializers.CharField(required=True)
    base_description = serializers.CharField(required=False)
    base_medium_only = serializers.BooleanField(required=False)
    base_group = serializers.CharField(required=True)
    base_type = serializers.CharField(required=True)
    base_price = serializers.FloatField(required=True)
    base_note = serializers.CharField(required=False)
    base_image = serializers.ImageField(required=False, read_only=True)
    
    class Meta:
        model = Base
        fields = (
            "base_name", 
            "base_group", 
            "base_type", 
            "base_price", 
            "base_description", 
            "base_note",
            "base_medium_only",
            "base_image"
        )
        extra_kwargs = {
            "base_image": {
                "validators": []
            }
        }
        
    # email = serializers.EmailField(required=True)
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(min_length=8, write_only=True)
    
    def validate(self, data):
        print("[validate]: inside validate")
        print(data)
        
        # initial data
        # initial_data = self.initial_data
        # print(initial_data)
        
        # save images
        
        
        return data

    def create(self, validated_data):
        # initial data
        initial_data = self.initial_data
        print(initial_data)
        
        # save validated data
        instance = self.Meta.model(**validated_data)
        
        # save images
        image = initial_data.get("base_image", None)
        if image != "null":
            instance.base_image = image
        instance.save()
        return instance
        # pass


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
