from django.contrib import admin
from .models import Category, Subcategory, Product


# Define the custom action to delete all products
def delete_all_products(modeladmin, request, queryset):
    Product.objects.all().delete()  # Deletes all Product instances
    modeladmin.message_user(request, "All products have been deleted.")


# Register the Product model in the admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'subcategory', 'image_path')

    # Add the custom action to the actions list
    actions = [delete_all_products]


# Register your models with the admin interface
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product, ProductAdmin)  # Register Product with ProductAdmin
