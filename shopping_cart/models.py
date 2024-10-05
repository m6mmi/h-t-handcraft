from django.contrib.auth.models import User
from django.db import models
from products.models import Product
from products.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cart id: {self.id}, user: {self.user}, date added: {self.date_added.strftime("%Y-%m-%d %H:%M:%S")}'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True)

    def total_item_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        user = self.cart.user
        return (f'[{user.first_name} {user.last_name}], {self.product.title}, {self.product.price}, '
                f'{self.product.stock}, {self.product.description}')
