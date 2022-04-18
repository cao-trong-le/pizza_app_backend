import random
import string
import json
import datetime


def generate_code(code_length):
    characters = string.ascii_letters + string.digits
    code = "".join(random.choices(characters, k=code_length))
    return f"#{code}"

# return an object


def handle_sauce(_sauce, _sauce_db):
    sauce_object = _sauce_db.objects.get(id=_sauce["id"])
    _sauce_amount = _sauce["amount"]
    sauce_note = json.dumps({"amount": _sauce_amount})

    return [sauce_note, sauce_object]

# return an object


def handle_dough(_dough, _dough_db):
    dough_object = _dough_db.objects.get(id=_dough["id"])
    dough_note = {}

    return [dough_note, dough_object]

# return an object


def handle_base_cheese(_base_cheese, _base_cheese_db):
    base_cheese_object = _base_cheese_db.objects.get(id=_base_cheese["id"])
    _base_cheese_amount = _base_cheese["amount"]
    base_cheese_note = json.dumps({"amount": _base_cheese_amount})

    return [base_cheese_note, base_cheese_object]

# return a list of objects


def handle_toppings(_toppings, _topping_db):
    topping_objects = []
    topping_notes = {}

    for topping in _toppings:
        topping_object = _topping_db.objects.get(id=int(topping["id"]))
        topping_objects.append(topping_object)
        topping_part = str(topping["part"])
        topping_amount = str(topping["amount"])

        topping_note = {
            "part": topping_part,
            "amount": topping_amount
        }

        topping_notes[topping["name"]] = json.dumps(topping_note)

    return [topping_notes, topping_objects]


# return a pizza object
def handle_pizza(pizza_db, _data, note_data, pizza_data):
    pizza_code = pizza_data.data["pizza_code"]
    pizza_object = pizza_db.objects.get(pizza_code=pizza_code)

    pizza_object.dough = _data["dough"]
    pizza_object.sauce = _data["sauce"]
    pizza_object.base_cheese = _data["base_cheese"]
    pizza_object.is_sample = False
    pizza_object.note = json.dumps(note_data)

    for topping in _data["toppings"]:
        pizza_object.toppings.add(topping)

    pizza_object.save()

    return pizza_object


def customize_and_create_pizza(pizza, topping_db, sauce_db, cheese_db, dough_db):
    pizza["name"] = pizza["name"] + generate_code(5)

    removed_attributes = [
        "id", "pizza_img", "pizza_code", "toppings", "dough", "sauce", "base_cheese"]
    noted_attributes = ["toppings",
                        "dough", "sauce", "base_cheese"]

    feature_data = {}
    pizza_note = {}
    _feature_data = None

    for attribute in removed_attributes:
        if attribute in noted_attributes:
            # separate toppings, handle topping data
            feature = pizza[attribute].copy()

            if attribute == "toppings":
                _feature_data = handle_toppings(feature, topping_db)

            elif attribute == "dough":
                _feature_data = handle_dough(feature, dough_db)

            elif attribute == "sauce":
                _feature_data = handle_sauce(feature, sauce_db)

            elif attribute == "base_cheese":
                _feature_data = handle_base_cheese(
                    feature, cheese_db)

            feature_data[attribute] = _feature_data[1]
            pizza_note[attribute] = _feature_data[0]

        del pizza[attribute]

    return pizza, feature_data, pizza_note


def add_items_to_order(pizza_objects, _order_data, _restaurant_id, order_db):
    order_code = _order_data.data["order_code"]
    order = order_db.objects.get(order_code=order_code)

    for pizza_object in pizza_objects:
        order.pizzas.add(pizza_object)

    order.order_finish = order.order_time + datetime.timedelta(minutes=20)
    order.restaurant_location = _restaurant_id
    order.save()

    return order.order_code
