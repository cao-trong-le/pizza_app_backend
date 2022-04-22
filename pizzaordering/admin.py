from django.contrib import admin
from .models import (
    Product, Base, Receipt, Order,
    SecretKeys
)

# Register your models here.
admin.site.register(Product)
admin.site.register(Base)
admin.site.register(Receipt)
admin.site.register(Order)
admin.site.register(SecretKeys)
