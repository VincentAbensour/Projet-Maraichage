from django.db import models
from account.models import Account
from producteur.models import Product, StockItem

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=300, blank=True)
    added_date = models.DateField(auto_now_add=True)
    cart_user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cart_user.firstname}'s Cart" if self.cart_user else f"Cart Number {self.cart_id}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    
    def __str__(self):
        return f"{self.stock_item.product_stockitem.name} Item"
    
    @property
    def get_total_price(self):
        return self.quantity*self.stock_item.product_stockitem.price



