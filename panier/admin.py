from django.contrib import admin
from . import models
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'is_ordered', 'is_ready')
    list_editable = ('is_ordered', 'is_ready')

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem)