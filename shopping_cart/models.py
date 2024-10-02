from django.db import models

from products.models import Product
from products.models import Product
from users.models import User


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cart id: {self.id}, user: {self.user}, date added: {self.date_added.strftime("%Y-%m-%d %H:%M:%S")}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    confirmation = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)

    # Shipping information

    # TODO: Create a separate model for shipping and billing
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=32, null=True)
    county = models.CharField(max_length=32, null=True)
    zipcode = models.CharField(max_length=16, null=True)
    country = models.CharField(max_length=32, null=True)
    phone_number = models.CharField(max_length=16, null=True)

    def __str__(self):
        return f'Order id: {self.id}, order date: {self.date_ordered.strftime("%Y-%m-%d")}, cart: {self.cart.id}'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        user = self.cart.user
        return (f'[{user.first_name} {user.last_name}], {self.product.title}, {self.product.price}, '
                f'{self.product.stock}, {self.product.description}')
