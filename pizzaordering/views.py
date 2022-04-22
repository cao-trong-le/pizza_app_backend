from .email_handler import send_email
from rest_framework import generics, status, permissions, viewsets
from django.http import HttpResponse

from .serializers import (
    ProductSerializer,
    BaseSerializer,
    OrderSerializer,
    ReceiptSerializer,
    SecretKeySerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Product, Base, Order, Dipping, Receipt, SecretKeys
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

class BaseView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BaseSerializer
    queryset = Base.objects.all()

class ProductView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, pizzaFavorite):
        if request.method == 'GET':
            pizzas = Product.objects.filter(
                pizza_type=pizzaFavorite, is_sample=True)

            if len(pizzas) > 0:
                data = self.serializer_class(pizzas, many=True).data

                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):
        if request.method == 'GET':
            orders = Order.objects.all()

            if len(orders) > 0:
                data = self.serializer_class(orders, many=True).data

                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if request.method == "POST":
            pass


class ReceiptView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def get(self, request):
        if request.method == 'GET':
            receipts = self.queryset

            if len(receipts) > 0:
                data = self.serializer_class(receipts, many=True)
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                return Response({"data": "None"}, status=status.HTTP_200_OK)

            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
