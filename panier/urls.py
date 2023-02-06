from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_view, name="market"),
    path('monpanier/', views.cart_view, name="cart"),

    path('validate_cart/', views.validate_cart_view, name="validate_cart"), 
    path('unvalidate_cart/', views.unvalidate_cart_view, name="unvalidate_cart"), 
         
    path('addtocart/<product_id>', views.add_to_cart_view, name="add_to_cart"),
    path('removefromcart/<product_id>', views.remove_from_cart_view, name="remove_from_cart"),     
]