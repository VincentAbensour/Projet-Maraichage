from django.http import HttpResponse
from django.shortcuts import render

from producteur.models import Product


def home_view(request):
    return render(request, "home.html")