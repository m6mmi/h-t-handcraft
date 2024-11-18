from django.contrib import admin
from .models import ShippingAddress, Order, Itella, Omniva

admin.site.register(Order)
admin.site.register(ShippingAddress)
# admin.site.register(Itella)
admin.site.register(Omniva)


class ItellaAdmin(admin.ModelAdmin):
    list_display = ('user', 'box_name', 'phone_number')


admin.site.register(Itella, ItellaAdmin)
