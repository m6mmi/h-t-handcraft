from itertools import product

from products.models import Product

from django.db import models
from users.models import User
from products.models import Product


# Create your models here.
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart id: {self.cart_id}, user: {self.user_id}, date added: {self.date_added.strftime("%Y-%m-%d %H:%M:%S")}'


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_id = models.AutoField(primary_key=True)
    confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f'Order id: {self.order_id}, user: {self.user_id}, date ordered: {self.date_ordered.strftime("%Y-%m-%d %H:%M:%S")}'


class CartProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        user = self.cart_id.user_id
        return f'[{user.first_name} {user.last_name}], {self.product_id.title}, {self.product_id.price}, {self.product_id.stock}, {self.product_id.description}'
