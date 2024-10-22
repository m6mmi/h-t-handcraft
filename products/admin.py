from django.contrib import admin
from .models import Category, Product, GalleryImage

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'image_path')
    list_editable = ('price', 'stock', 'image_path')


admin.site.register(Product, ProductAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

admin.site.register(GalleryImage, GalleryImageAdmin)
