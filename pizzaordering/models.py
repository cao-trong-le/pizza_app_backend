from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid
import random
import string
import datetime

# Create your models here.

# plan: resize and upload image to aws storage

# User = settings.AUTH_USER_MODEL
User = get_user_model()


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


#Dough, Cheese, Sauce, Topping are pizza ingredients and bases
# name, medium_only, group, type, image, price, special_instructions, 

class Base(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255, null=False, unique=True)
    medium_only = models.BooleanField(verbose_name="Medium Only", default=False)
    group_options = (
        ("dough", "Dough"), 
        ("sauce", "Sauce"),
        ("cheese", "Cheese"), 
        ("topping", "Topping")
    )
    group = models.CharField(max_length=100, default="dough", choices=group_options)
    type_options = (
        ("none", "None"),
        ("meat", "Meat"),
        ("veggie", "Veggie"),
        ("cheese", "Cheese")
    )  
    type = models.CharField(
        verbose_name="Type",
        max_length=255, 
        default="None", 
        null=False, 
        choices=type_options
    )
    image = models.ImageField(
        verbose_name="Base Image", 
        upload_to=get_image_filepath, 
        null=True, 
        default=default_image
    )
    price = models.FloatField(verbose_name="Price", default=0.0)
    _carlos = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    carlos = models.CharField(verbose_name="Carlos", max_length=255, null=False, default=_carlos)
    special_instruction = models.CharField(verbose_name="Special Instruction", max_length=255, null=True, default="")
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False, unique=True)
    product_code = models.CharField(
        max_length=15, null=False, unique=True, default=generate__code)
    product_descritpion = models.CharField(max_length=255, null=False, unique=True)
    product_sizes = (
        ("none", "None"),
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
        ("extra-large", "Extra large")
    )
    product_slices = '''{ "small": 6, "medium": 8, "large": 10, "x-large": 12}'''
    product_prices = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    product_cals = '''{"small": 0, "medium": 0, "large": 0, "x-large": 0}'''
    product_img = models.ImageField(
        verbose_name="Product Image",
        upload_to=get_image_filepath,
        null=True,
        default=default_image
    )
    product_groups = (
        ("none", "None"),
        ("pizza", "Pizza"),
        ("drink", "Drink"),
        ("dipping", "Dipping")
    )
    product_group = models.CharField(max_length=100, null=True, default="", choices=product_groups)
    product_types = [
        ("none", "None"),
        ("pizza", (
                ("meat", "Meat"),
                ("veggie", "Veggie"),
                ("cheese", "Cheese"),
            )
        ),
        ("drink", (
                ("soft", "Soft"),
                ("tea", "Tea"),
                ("alcohol", "Alcohol"),
            )
         ),
        ("dipping", "None"),
    ]
    product_type = models.CharField(max_length=100, null=True, default="------", blank=False, choices=product_types)
    product_size = models.CharField(max_length=100, default="n", choices=product_sizes)
    product_slice = models.CharField(max_length=255, default=product_slices, null=True)
    product_is_sample = models.BooleanField(default=False)
    product_base = models.ManyToManyField(to=Base, blank=True)
    product_carlos = models.CharField(max_length=255, null=False, default=product_cals)
    product_price = models.CharField(max_length=255, null=False, default=product_prices)
    product_note = models.CharField(max_length=550, default="", blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_code = models.CharField(
        max_length=15, null=False, unique=True, default=generate__code)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    product = models.ManyToManyField(
        to=Product, related_name="order_pizza", blank=True)
    is_delivery = models.BooleanField(default=False)
    is_pickup = models.BooleanField(default=False)
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
