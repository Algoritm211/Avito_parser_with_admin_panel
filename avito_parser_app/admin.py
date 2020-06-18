from django.contrib import admin
from .models import Product
from .forms import ProductForm

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'currency', 'published_date', 'url')
    list_filter = ('currency', 'published_date')
    form = ProductForm