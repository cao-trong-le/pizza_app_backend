from .email_handler import send_email
from rest_framework import generics, status, permissions, viewsets
from django.http import HttpResponse

from .serializers import (
    PizzaSerializer,
    ToppingSerializer,
    SauceSerializer,
    CheeseSerializer,
    DoughSerializer,
    DippingSerializer,
    OrderSerializer,
    ReceiptSerializer,
    SecretKeySerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Pizza, Topping, Dough, Order, Dipping,
    Sauce, Receipt, Cheese, SecretKeys
)
import datetime
import json

from django.contrib.auth.models import User
from ._tools import generate_code
from ._tools import (
    handle_pizza,
    add_items_to_order,
    customize_and_create_pizza
)

from .google_api import GoogleAPI

# stripe
import stripe
stripe.api_key = "*******************"

# email


class RetrieveKeys(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SecretKeySerializer
    queryset = SecretKeys.objects.all()

    def get(self, request, key_name):
        key = self.queryset.get(name=key_name)
        data = self.serializer_class(instance=key).data

        return Response({"key": data}, status=status.HTTP_200_OK)


class CreatePayment(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.method == "POST":
            data = request.data
            order_code = data["order_code"]

            order = Order.objects.get(order_code=order_code)
            receipt = order.pizza_order

            customer_data = json.loads(data["customer_data"])
            payment_data = json.loads(data["payment_data"])

            if payment_data:
                customer = stripe.Customer.create(
                    email=customer_data["email"],
                    name=customer_data["f_name"],
                    source=payment_data["token"]
                )

                peny_price = receipt.after_tax * 100

                charge = stripe.Charge.create(
                    customer=customer,
                    amount=int(f"{peny_price:.0f}"),
                    currency='cad',
                    description="Pizza Payment"
                )

            send_email_to_user = send_email()

            return Response({"data": "data went through"}, status=status.HTTP_200_OK)


class FindNearestRestaurants(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.method == "POST":
            data = json.loads(request.data["data"])
            location = None
            google_api = GoogleAPI()

            print(request.data)

            if data["search_type"] == "by_provided_location":
                returned_data = google_api.extract_coors_from_address(
                    data["address"])

                if bool(returned_data):
                    location = google_api.extract_coors_from_address(
                        data["address"])["location"]

                else:
                    return Response(
                        {
                            "data": {
                                "available_location": [],
                                "message": "Oops, Not found!! Please, enter a valid address"
                            }
                        },
                        status=status.HTTP_200_OK
                    )

            else:
                location = data["location"]

            nearest_restaurants = google_api.get_nearby_place(
                radius=2500,
                _type="restaurant",
                keyword="pizza pizza",
                location=location
            )

            # print(nearest_restaurants["available_location"])

            place_details = google_api.place_detail(
                nearest_restaurants["available_location"])

            if len(nearest_restaurants["available_location"]) > 0:
                destinations = []

                for restaurant in nearest_restaurants["available_location"]:
                    r_location = restaurant["geometry"]["location"]
                    destinations.append(r_location)

                _distances = google_api.distance_calculation(
                    origin=location, destinations=destinations)

                print(len(_distances["rows"][0]["elements"]))

                element_counter = len(_distances["rows"][0]["elements"])
                elements = _distances["rows"][0]["elements"]

                for i in range(element_counter):
                    nearest_restaurants["available_location"][i]["distance"] = elements[i]["distance"]
                    nearest_restaurants["available_location"][i]["details"] = place_details[i]

                return Response({"data": nearest_restaurants}, status=status.HTTP_200_OK)

            else:
                return Response(
                    {
                        "data": {
                            "available_location": [],
                            "message": """ Oops, Not found!! There is no restaurant within 2.5 km more or less."""
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCustomizedPizza(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()


class RetrievePizza(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

    def get(self, request, pizzaFavorite):
        if request.method == 'GET':
            pizzas = Pizza.objects.filter(
                pizza_type=pizzaFavorite, is_sample=True)

            if len(pizzas) > 0:
                data = PizzaSerializer(pizzas, many=True).data

                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDough(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = DoughSerializer
    queryset = Dough.objects.all()

    def get(self, request):
        if request.method == 'GET':
            print(self.queryset.all())

            if len(self.queryset.all()) > 0:
                data = self.serializer_class(
                    self.queryset.all(), many=True).data
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveSauce(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SauceSerializer
    queryset = Sauce.objects.all()

    def get(self, request):
        if request.method == 'GET':
            sauces = Sauce.objects.all()

            if len(self.queryset.all()) > 0:
                data = SauceSerializer(self.queryset.all(), many=True).data
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveTopping(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ToppingSerializer
    queryset = Topping.objects.all()

    def get(self, request):
        if request.method == 'GET':
            toppings = Topping.objects.all()

            if len(toppings) > 0:
                data = ToppingSerializer(toppings, many=True).data
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDipping(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = DippingSerializer
    queryset = Dipping.objects.all()

    def get(self, request):
        if request.method == 'GET':
            dippings = self.queryset.all()

            if len(dippings) > 0:
                data = PizzaSerializer(dippings, many=True).data

                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCheese(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CheeseSerializer
    queryset = Cheese.objects.all()

    def get(self, request):
        if request.method == 'GET':
            print("get cheese")
            cheeses = self.queryset.all()

            if len(cheeses) > 0:
                data = CheeseSerializer(cheeses, many=True).data
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveOrder(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):
        if request.method == 'GET':
            orders = Order.objects.all()

            if len(orders) > 0:
                data = PizzaSerializer(orders, many=True)

                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class PlaceOrder(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReceiptSerializer
    queryset = Order.objects.all()

    def post(self, request):
        if request.method == "POST":
            if request.data:
                # create an order
                user = User.objects.get(id=1)
                order_data = {"customer": user.id}
                _order_data = OrderSerializer(data=order_data)
                _restaurant_id = json.loads(
                    request.data["selected_restaurant"])["place_id"]

                if _order_data.is_valid():
                    _order_data.save()

                # create new customized pizzas
                _pizza_is_valid = 0
                pizzas = json.loads(request.data["pizzas"])
                _pizza_objects = []

                for pizza in pizzas:
                    _pizza = customize_and_create_pizza(
                        pizza=pizza, topping_db=Topping, sauce_db=Sauce, cheese_db=Cheese, dough_db=Dough)

                    pizza_data = PizzaSerializer(data=_pizza[0])

                    if not pizza_data.is_valid():
                        return Response(
                            {"data": {"message": pizza_data.errors}},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        )

                    _pizza_is_valid += 1
                    pizza_data.save()

                    pizza_object = handle_pizza(pizza_db=Pizza, _data=_pizza[1],
                                                note_data=_pizza[2], pizza_data=pizza_data)

                    _pizza_objects.append(pizza_object)

                if _pizza_is_valid == len(pizzas):
                    _order_code = add_items_to_order(
                        pizza_objects=_pizza_objects,
                        _order_data=_order_data,
                        _restaurant_id=_restaurant_id,
                        order_db=Order
                    )

                    return Response(
                        {
                            "data": {
                                "message": "Your order has been placed",
                                "order_code": _order_code
                            }
                        },
                        status=status.HTTP_200_OK
                    )

            return Response(
                {"data": {"message": "bad request"}},
                status=status.HTTP_400_BAD_REQUEST
            )


class RetrieveReceipt(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def get(self, request):
        if request.method == 'GET':
            receipts = Receipt.objects.all()

            if len(receipts) > 0:
                data = PizzaSerializer(receipts, many=True)
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
