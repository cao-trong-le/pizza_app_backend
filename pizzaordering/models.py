from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid
import random
import string
import datetime
import functools

from pkg_resources import require


# Create your models here.

# plan: resize and upload image to aws storage

# User = settings.AUTH_USER_MODEL
User = get_user_model()

characters = string.ascii_letters + string.digits + string.punctuation

def generate__base_code():
    flag_check = True
    _code = None
    display_code = None
    _code_list = Base.objects.values_list("base_code", flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=8))
        display_code = f"#BASE{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code

def generate__product_code():
    flag_check = True
    _code = None
    display_code = None
    _code_list = Product.objects.values_list("product_code", flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=10))
        display_code = f"#PRODUCT{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code

def generate__order_code():
    flag_check = True
    _code = None
    display_code = None
    _code_list = Order.objects.values_list("product_code", flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=10))
        display_code = f"#ORDER{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code


def generate__receipt_code():
    flag_check = True
    _code = None
    display_code = None
    _code_list = Receipt.objects.values_list("product_code", flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=12))
        display_code = f"#RECEIPT{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code

def default_image():
    return f"default_image/default.png"


def get_image_filepath(instance, filename):
    obj_class_name = instance.__class__.__name__
    valid_class_names = ["Product", "Base"]
    _index = valid_class_names.index(obj_class_name)
    _lowered_class_name = valid_class_names[_index].lower()
    return f"{_lowered_class_name}_images/{filename}"


#Dough, Cheese, Sauce, Topping are pizza ingredients and bases
# name, medium_only, group, type, image, price, special_instructions, 

class Base(models.Model):
    id = models.AutoField(primary_key=True)
    base_code = models.CharField(max_length=15, null=False, unique=True, default=generate__base_code)
    base_name = models.CharField(verbose_name="Name", max_length=255, null=False, unique=True)
    base_description = models.CharField(max_length=255, null=True, default="")
    base_medium_only = models.BooleanField(verbose_name="Medium Only", default=False)
    group_options = (
        ("dough", "Dough"), 
        ("sauce", "Sauce"),
        ("cheese", "Cheese"), 
        ("topping", "Topping")
    )
    base_group = models.CharField(max_length=100, default="dough", choices=group_options)
    type_options = (
        ("none", "None"),
        ("meat", "Meat"),
        ("veggie", "Veggie"),
        ("cheese", "Cheese")
    )  
    base_type = models.CharField(
        verbose_name="Type",
        max_length=255, 
        default="None", 
        null=False, 
        choices=type_options
    )
    base_image = models.ImageField(
        verbose_name="Base Image", 
        upload_to=get_image_filepath, 
        null=True, 
        default=default_image
    )
    base_price = models.DecimalField(verbose_name="Price", max_digits=10, default=0.0, decimal_places=2)
    base_note = models.CharField(verbose_name="Special Instruction", max_length=255, null=True, default="")
    
    def __str__(self):
        return self.base_name
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=15, null=False, unique=True, default=generate__product_code)
    product_name = models.CharField(max_length=100, null=False, unique=True)
    product_descritpion = models.CharField(max_length=255, null=True, default="")
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
    product_base = models.ManyToManyField(to=Base, blank=True, related_name="product_base")
    product_carlos = models.CharField(max_length=255, null=False, default=product_cals)
    product_price = models.CharField(max_length=255, null=False, default=product_prices)
    product_discount = models.FloatField(verbose_name="Product Discount", default=0)
    product_note = models.CharField(max_length=550, default="", blank=True, null=True)
    product_created_date = models.DateTimeField(verbose_name="Product Created Date", auto_now=True)
    product_updated_date = models.DateTimeField(verbose_name="Product Updated Date", default=datetime.datetime.now)
    
    def __str__(self):
        return self.product_name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_code = models.CharField(max_length=15, null=False, unique=True, default=generate__order_code)
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
    id = models.AutoField(primary_key=True)
    receipt_code = models.CharField(max_length=15, null=False, unique=True, default=generate__receipt_code)
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
