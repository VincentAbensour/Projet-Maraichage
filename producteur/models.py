import datetime
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    unit_choices = [
        ('Kg', 'Kg'),
        ('G', 'G'),
        ('Pce', 'Pce'),
    ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,blank=True, null=True)
    price = models.FloatField()
    unit = models.CharField(max_length=50, choices=unit_choices, default='Kg')
    slug = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='media/products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Week(models.Model):
    class Meta:
      get_latest_by = 'created_date'

    created_date = models.DateTimeField(auto_now_add=True)
    end_shopping_date = models.DateTimeField()

    @property
    def get_week_number(self):
        return self.created_date.isocalendar()[1]

    def __str__(self):
        return f'Semaine numéro {self.get_week_number}'

def get_week():
    return Week.objects.latest().id

class StockItem(models.Model):
    product_stockitem = models.ForeignKey(Product, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, default = get_week )
    stock = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock de {self.product_stockitem.name}"
    
    

    

    