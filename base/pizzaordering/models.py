from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string
import datetime

# Create your models here.


def generate__code():
    characters = string.ascii_letters + string.digits
    _code = "".join(random.choices(list(characters), k=14))
    return f"#{_code}"


def default_image():
    return f"default_image/default.png"


def get_image_filepath(instance, filename):
    obj_name = instance.name
    obj_name = obj_name.lower().split(" ")
    obj_name = "_".join(obj_name)

    obj_class_name = instance.__class__.__name__

    valid_class_names = ["Pizza", "Topping",
                         "Dipping", "Dough", "Sauce", "Cheese"]
    _index = valid_class_names.index(obj_class_name)
    _lowered_class_name = valid_class_names[_index].lower()

    return f"{_lowered_class_name}_images/{obj_name}/{filename}"


class Dough(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    medium_only = models.BooleanField(default=False)
    dough_img = models.ImageField(
        verbose_name="dough image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    _carlos = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    carlos = models.CharField(max_length=255, null=False, default=_carlos)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Sauce(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    _am = (
        ("less", "Less"),
        ("more", "More"),
        ("regular", "Regular"),
    )
    amount = models.CharField(
        max_length=20, null=False, default="regular", choices=_am)
    sauce_img = models.ImageField(
        verbose_name="sauce image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    _carlos = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    carlos = models.CharField(max_length=255, null=False, default=_carlos)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Cheese(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    _am = (
        ("less", "Less"),
        ("more", "More"),
        ("regular", "Regular"),
    )
    amount = models.CharField(
        max_length=20, null=False, default="regular", choices=_am)
    cheese_img = models.ImageField(
        verbose_name="cheese image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    _carlos = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    carlos = models.CharField(max_length=255, null=False, default=_carlos)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Dipping(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    dipping_img = models.ImageField(
        verbose_name="dipping image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    number = models.IntegerField(default=0)
    carlos = models.IntegerField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    topping_category = (
        ("meat", "Meat"),
        ("veggie", "Veggie"),
        ("cheese", "Cheese"),
    )
    category = models.CharField(
        max_length=10, null=False, choices=topping_category)
    topping_img = models.ImageField(
        verbose_name="topping image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    _carlos = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    carlos = models.CharField(max_length=255, null=False, default=_carlos)
    parts = (
        ("left side", "Left Side"),
        ("on whole", "On Whole"),
        ("right side", "Right Side"),
    )
    part = models.CharField(max_length=20, null=False,
                            default="on whole", choices=parts)
    _am = (
        ("less", "Less"),
        ("more", "More"),
        ("regular", "Regular"),
    )
    amount = models.CharField(
        max_length=20, null=False, default="regular", choices=_am)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    pizza_code = models.CharField(
        max_length=15, null=False, unique=True, default=generate__code)
    pizza_sizes = (
        ("s", "Small"),
        ("m", "Medium"),
        ("l", "Large"),
        ("x", "Extra large")
    )

    pizza_slices = '''{ "small": 6, "medium": 8, "large": 10, "x-large": 12}'''

    pizza_prices = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''

    pizza_cals = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''

    pizza_img = models.ImageField(
        verbose_name="pizza image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    pizza_type = models.CharField(max_length=100, null=False, default="meat")
    size = models.CharField(max_length=1, default="s", choices=pizza_sizes)
    slices = models.CharField(max_length=255, default=pizza_slices, null=False)
    is_sample = models.BooleanField(default=False)
    toppings = models.ManyToManyField(to=Topping, blank=True)
    dough = models.ForeignKey(to=Dough, null=True, on_delete=models.CASCADE)
    sauce = models.ForeignKey(to=Sauce, null=True, on_delete=models.CASCADE)
    base_cheese = models.ForeignKey(
        to=Cheese, null=True, on_delete=models.CASCADE)
    carlos = models.CharField(max_length=255, null=False, default=pizza_cals)
    number = models.IntegerField(default=1, null=True)
    price = models.CharField(max_length=255, null=False, default=pizza_prices)
    note = models.CharField(max_length=550, default="", blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_code = models.CharField(
        max_length=15, null=False, unique=True, default=generate__code)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    pizzas = models.ManyToManyField(
        to=Pizza, related_name="order_pizza", blank=True)
    dippings = models.ManyToManyField(
        to=Dipping, related_name="order_dipping", blank=True)
    is_delivery = models.BooleanField(default=False)
    restaurant_location = models.CharField(
        max_length=250, default="", null=True, blank=True)
    delivery_location = models.CharField(
        max_length=250, default="", null=True, blank=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_finish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_code


class Receipt(models.Model):
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    order = models.OneToOneField(
        to=Order,
        related_name="pizza_order",
        blank=True,
        default="",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    tax = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    after_tax = models.DecimalField(max_digits=10, decimal_places=2)


class SecretKeys(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    key = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=255, default="")

    def __str__(self):
        return self.name
