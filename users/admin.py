from django.contrib import admin
from .models import  ShippingAddress, Order

admin.site.register(Order)
admin.site.register(ShippingAddress)
