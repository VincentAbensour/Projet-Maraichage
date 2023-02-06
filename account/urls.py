from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('login', views.login_view, name="login"),
   path('logout', views.logout_view, name="logout"),
   path('register', views.register_view, name="register"),
   path('activate/<uidb64>/<token>', views.activate_view, name="activate"),
]
