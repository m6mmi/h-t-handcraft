from enum import unique

from django.db import models
from users import User
from products import Product


# Create your models here.
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_id = models.AutoField(max_length=50, primary_key=True)
    confirmation = models.BooleanField(default=False)


class CartProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product