from django.contrib.auth.models import User
from django.db import models

from shopping_cart.models import Cart


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    zipcode = models.CharField(max_length=10, blank=False)
    county = models.CharField(max_length=25, blank=False)
    country = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        abstract = True


class Order(Address, models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    confirmation = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Order id: {self.id}, order date: {self.date_ordered.strftime("%Y-%m-%d")}, cart: {self.cart.id}'


class ShippingAddress(Address, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"
