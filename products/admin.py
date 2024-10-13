from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'image_path')
    list_editable = ('price', 'stock', 'image_path')


admin.site.register(Product, ProductAdmin)
