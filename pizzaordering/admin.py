from django.contrib import admin
from .models import (
    Pizza, Dipping, Sauce, Dough,
    Cheese, Topping, Receipt, Order,
    SecretKeys
)

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Dipping)
admin.site.register(Sauce)
admin.site.register(Dough)
admin.site.register(Cheese)
admin.site.register(Topping)
admin.site.register(Receipt)
admin.site.register(Order)
admin.site.register(SecretKeys)
