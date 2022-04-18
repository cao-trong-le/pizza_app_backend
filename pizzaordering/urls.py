from django.urls import path, re_path
from . import views

urlpatterns = [
    path('pizzas/dough/', views.RetrieveDough.as_view(),
         name="retrieve-dough"),
    path('pizzas/sauce/', views.RetrieveSauce.as_view(), name="retrieve-sauce"),
    path('pizzas/dippings/', views.RetrieveDipping.as_view(),
         name="retrieve-dippings"),
    path('pizzas/cheeses/', views.RetrieveCheese.as_view(),
         name="retrieve-cheeses"),
    path('pizzas/topping/', views.RetrieveTopping.as_view(),
         name="retrieve-topping"),
    path('pizzas/<str:pizzaFavorite>/',
         views.RetrievePizza.as_view(), name="retrieve-pizza"),
    path('pizza/order/', views.PlaceOrder.as_view(),
         name="place-order"),
    path('nearest_stores/', views.FindNearestRestaurants.as_view(),
         name="fetch-restaurant"),
    path('charge_pizza/', views.CreatePayment.as_view(), name="pizza-payment"),
    path('get_keys/<str:key_name>/',
         views.RetrieveKeys.as_view(), name="pizza-keys"),
]
