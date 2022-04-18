from rest_framework import serializers
from .models import (
    Pizza, Topping, Dough, Order, Dipping,
    Sauce, Receipt, Cheese, SecretKeys
)
from rest_framework.serializers import ValidationError
from rest_framework.serializers import (
    ValidationError,
    SerializerMethodField,
    HyperlinkedModelSerializer
)


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = "__all__"
        depth = 2


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = "__all__"


class DoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dough
        fields = "__all__"


class DippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dipping
        fields = "__all__"


class SauceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauce
        fields = "__all__"


class CheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
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
