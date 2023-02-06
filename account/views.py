from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from panier.models import Cart, CartItem
from .models import Account
from panier.views import get_session
from account.form import RegisterForm

#import for email verification
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def login_view(request):

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
     
        try:
            user = Account.objects.get(email=email)     
        except:
            messages.error(request,'Adresse Mail Inconnue')
            return redirect("login")
        
        if check_password(password, user.password):    
            user = auth.authenticate(email=email, password=password)
        else:
            messages.error(request,'Mauvais Mot De Passe')
            return redirect("login")
                
        # Transférer le cart de la session au cart de l'utilisateur       
        try:
            session_cart = Cart.objects.get(cart_id = get_session(request))  
        except Cart.DoesNotExist:
            session_cart = None
        
        if user is not None:
            if session_cart is not None:     
                try: # Si l'utilisateur avait déjà un panier on fusionne les deux  
                    user_cart = Cart.objects.get(cart_user = user)
                    if user_cart.is_ordered:
                        messages.error(request,'Vous avez déjà un panier validé. Votre panier actuel n\'a pas été modifié')
                        print('Vous avez déjà un panier validé')
                        session_cart.delete()
                    else:
                        session_item = CartItem.objects.filter(cart = session_cart)
                        user_item = CartItem.objects.filter(cart = user_cart)
                        product_in_cart = [item.stock_item.product_stockitem.name for item in user_item]
                        # On loop dans la liste d'item de session
                        for item in session_item:
                        # Pour chaque item, si son nom est déjà présent dans le panier de l'utilisateur on incrément sa quantité  
                            if item.stock_item.product_stockitem.name in product_in_cart:
                                user_unique_item = CartItem.objects.get(cart = user_cart, stock_item = item.stock_item )
                                user_unique_item.quantity += item.quantity
                                user_unique_item.save()
                        # Sinon on lie l'item avec le panier de l'utilisateur à la place du panier de session
                            else:
                                item.cart = user_cart
                                item.save()
                        session_cart.delete()  
                except Cart.DoesNotExist: # Si l'utilisateur n'avait pas de panier on lie celui qu'il avait créé hors session avec son compte                   
                    session_cart.cart_user = user
                    session_cart.save()      
            else : # Si l'utilisateur n'avait pas de panier hors connexion on vérifie si il a un panier d'utilisateur
                try:
                    user_cart = Cart.objects.get(cart_user = user)  
                except Cart.DoesNotExist: # Sinon on lui en créé un 
                    user_cart = Cart.objects.create(cart_user = user, cart_id = get_session(request)) 
                    user_cart.save() 
                
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('login')   
    return render(request, "account/login.html")

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('home')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("firstname")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = Account.objects.create_user(
                    firstname= firstname,
                    lastname = lastname,
                    username = username,
                    email = email,
                    password = password,
                    )
            user.save()

            # Email Validation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            email_from = settings.EMAIL_HOST_USER
            message = render_to_string('account/account_verification_email.html', {
                'user' : user,
                'domaine' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' :  default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, email_from, to=[email])
            send_email.send()
            return redirect("/compte/login?command=verification&email="+email)
    else:
        form = RegisterForm

    context = {
        'form' : form
    }
    return render(request, 'account/register.html', context)


def activate_view(request, uidb64, token):
    try:
        uidb64 = urlsafe_base64_decode(uidb64)
        user = Account.objects.get(pk = uidb64)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé')
    else:
        messages.error(request, 'Votre compte n\'a pas été validé, le lien que vous avez utilisé n\'est pas valide')
        return redirect("register")
    
    return redirect("login")

