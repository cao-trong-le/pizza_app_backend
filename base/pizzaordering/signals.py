from .models import Order, Receipt
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.forms.models import model_to_dict
import json


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if not created:
        if instance.pizzas is not None:
            total = 0

            for pizza in model_to_dict(instance)["pizzas"]:
                price = list(json.loads(pizza.price).items())[0][1]
                number = pizza.number
                total += price * number

            tax = total * 0.13
            after_tax = total + tax

            create_new_receipt = Receipt(
                customer=instance.customer,
                order=instance,
                price=total,
                tax=tax,
                after_tax=after_tax
            )

            create_new_receipt.save()
