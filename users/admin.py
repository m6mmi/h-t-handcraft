from django.contrib import admin
from .models import  ShippingAddress, Order

# Register your models here.
admin.site.register(Order)
admin.site.register(ShippingAddress)
