from django.contrib import admin
from .models import Cart, CartProduct

admin.site.register(CartProduct)


class CartProductInline(admin.StackedInline):
    model = CartProduct
    can_delete = True
    verbose_name_plural = 'Tooted'
    verbose_name = 'Toode'
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [CartProductInline]


admin.site.register(Cart, CartAdmin)
