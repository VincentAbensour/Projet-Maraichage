from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_editable = ('is_available',)

class StockItemAdmin(admin.ModelAdmin):
    list_display = ('product_stockitem', 'week', 'stock', 'is_active')
    list_editable = ('stock', 'is_active',)

class WeekAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'end_shopping_date')

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.StockItem, StockItemAdmin)
admin.site.register(models.Week, WeekAdmin)