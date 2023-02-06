from smtplib import SMTPException
from django.shortcuts import redirect, render
from panier.models import Cart, CartItem
from django.contrib.auth.decorators import user_passes_test
from producteur.models import Week
from babel.dates import format_datetime
from django.contrib import messages

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='market')
def dashboard_view(request):
    try:
        carts = Cart.objects.filter(cart_user__isnull = False, is_ordered = True)
        cartitems = CartItem.objects.filter(cart__is_ordered = True)
        week = Week.objects.latest('created_date')
        end_shopping_date = format_datetime(week.end_shopping_date, locale='fr')
    except Cart.DoesNotExist:
        carts = None
    except CartItem.DoesNotExist:
        cartitems = None
    except Week.DoesNotExist:
        week = None
        end_shopping_date = ""
    
    # Pour le récapitulatif des paniers:
    # Différencier les items de chaque panier et leur attribuer leur quantité dans un dictionnaire.
    vegetables_dict = {}
    for item in cartitems:
        if item.stock_item.product_stockitem.name in vegetables_dict:
            vegetables_dict[item.stock_item.product_stockitem.name] += item.quantity
        else :
            vegetables_dict[item.stock_item.product_stockitem.name] = item.quantity

    context = {
        'week' : week,
        'end_shopping_date' : end_shopping_date,
        'carts' : carts,
        'items' : vegetables_dict,
    }
    return render(request, "maraicher/dashboard.html", context) 

def cart_detail_view(request, cart_id):
    try:
        cart = Cart.objects.get(cart_id = cart_id ) 
        cartitems = CartItem.objects.filter(cart = cart)
        cart_price = sum([item.get_total_price for item in cartitems])
    except Cart.DoesNotExist:
        cart = None
    except CartItem.DoesNotExist:
        cartitems = None
        cart_price = "0"

    context = {
        "cart" : cart,
        "cartitems" : cartitems,
        'cart_price' : cart_price
    }

    return render(request, "maraicher/cart_detail.html", context) 

def validate_cart_view(request, cart_id):
    cart = Cart.objects.get(cart_id = cart_id )   
    user = cart.cart_user

    cartitems = CartItem.objects.filter(cart = cart)
    cart_price = sum([item.get_total_price for item in cartitems])
 
    try:
        mail_subject = 'Votre Panier est prêt'
        email_from = settings.EMAIL_HOST_USER
        message = render_to_string('maraicher/cart_ready_email.html', {
                    'user' : user,
                    'cart_price' : cart_price,
                })
        send_email = EmailMessage(mail_subject, message, email_from, to=[user.email])
        send_email.send()
    except SMTPException:
        messages.error(request,"Problème lors de l'envoie du mail, vérifiez la validité de l'adresse. Le panier n'a pas été validé")
    else:
        cart.is_ready = True
        cart.save()

    return redirect('dashboard')