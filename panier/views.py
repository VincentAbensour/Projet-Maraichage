from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from babel.dates import format_datetime
from datetime import datetime

from panier.models import Cart, CartItem
from producteur.models import StockItem, Week


def get_session(request):
    session_key = request.session.session_key
    if session_key is None:
        request.session.create()
        session_key = request.session.session_key
    return session_key

def get_or_create_cart(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            cart = Cart.objects.get(cart_user = user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = user)
            cart.save()
    else:
        try:
            cart = Cart.objects.get(cart_id = get_session(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = get_session(request))
            cart.save()
    return cart

def market_view(request):
    user = request.user
    try:
        stockitem = StockItem.objects.filter(week__end_shopping_date__gt = datetime.now())
    except StockItem.DoesNotExist:
        stockitem = {}

    if user.is_authenticated:
        is_ordered = Cart.objects.filter(cart_user = user, is_ordered = True).exists()
    else:
        is_ordered = False

    context = {
        "is_ordered" : is_ordered,
        "products" : stockitem
    }
    return render(request, "market/market.html", context)
    
def cart_view(request):

    cart = get_or_create_cart(request)

    try:
        week = Week.objects.latest('created_date')
        end_shopping_date = format_datetime(week.end_shopping_date, locale='fr')
        shopping_active = end_shopping_date < format_datetime(datetime.now(), locale='fr')
    except Week.DoesNotExist:
        week = None
        end_shopping_date = ""
        shopping_active = False

    try: 
        items = CartItem.objects.filter(cart = cart)
        total_price = sum([item.quantity*item.stock_item.product_stockitem.price for item in items])
    except CartItem.DoesNotExist:
        items = None
        total_price = "0"
    
    context = {
        "total_price" : total_price,
        "end_shopping_date": end_shopping_date,
        "shopping_active" : shopping_active,
        "cart" : cart,
        "products" : items
    }
    return render(request, "cart/cart.html", context)

def add_to_cart_view(request, product_id):
    cart = get_or_create_cart(request)

    try:
        stock_item = StockItem.objects.get(id=product_id)
        quantity = float(request.POST["item-quantity"])
    except (StockItem.DoesNotExist, ValueError):
        return redirect('market')

    # Vérifier si l'item ajouté est déjà dans le panier ou non
    item_to_add_exists = CartItem.objects.filter(cart = cart, stock_item = stock_item).exists()
    if item_to_add_exists: # Si c'est le cas on inrémente sa quantité dans le panier
        item_to_change = CartItem.objects.get(cart = cart, stock_item = stock_item)
        item_to_change.quantity += quantity
        item_to_change.save()
    else: # Sinon on créé un nouveau CartItem relié au cart actuel
        item_to_add = CartItem.objects.create(cart = cart, stock_item = stock_item, quantity = quantity)
        item_to_add.save()     
    return redirect('market')


def remove_from_cart_view(request, product_id):
    try:
        item = CartItem.objects.get(id = product_id)
    except CartItem.DoesNotExist:
        return redirect('cart')
    item.delete()
    return redirect('cart')

@login_required
def validate_cart_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(cart_user = user)
    except Cart.DoesNotExist:
        return redirect('cart')
    try:
        items = CartItem.objects.filter(cart = cart)
    except CartItem.DoesNotExist:
        return redirect('cart')

    #Vérifier s'il y a bien le stock nécessaire de StockItem pour chaque CartItem
    valid_cart = True
    for item in items:
        if item.stock_item.stock < item.quantity:
            valid_cart = False

    #Si c'est le cas pour chaque CartItem on répercute la quantité sur le stock du StockItem correspondant
    if valid_cart == True:
        for item in items:
            item.stock_item.stock -= item.quantity
            item.stock_item.save()
        cart.is_ordered = True
        cart.save()
    else:
        messages.error(request,"L'un de vos articles n'est plus disponible en quantité suffisante")

    return redirect('cart')

@login_required
def unvalidate_cart_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(cart_user = user)
        cart.is_ordered = False
        cart.save()
    except Cart.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            items = CartItem.objects.filter(cart = cart)
        except CartItem.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            for item in items:
                item.stock_item.stock += item.quantity
                item.stock_item.save()
    
    return redirect(request.META.get('HTTP_REFERER'))
 