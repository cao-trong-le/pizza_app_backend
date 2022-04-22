from django.urls import path, re_path
from . import views

urlpatterns = [
    path('product/', views.ProductView.as_view(),
         name="product-view"),
    path('product/base/', views.BaseView.as_view(),
         name="base-view"),
    path('order/', views.OrderView.as_view(),
         name="order-view"),
    path('receipt/', views.ReceiptView.as_view(), name="receipt-view"),
    path('nearest_stores/', views.FindNearestRestaurants.as_view(),
         name="fetch-restaurant"),
    path('product_checkout/', views.CreatePayment.as_view(), name="product-payment"),
]
