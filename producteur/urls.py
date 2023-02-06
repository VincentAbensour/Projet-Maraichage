from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('panier/<str:cart_id>/', views.cart_detail_view, name="cart_detail"),
    path('panier/valider/<str:cart_id>/', views.validate_cart_view, name="validate_cart"),
    
]