from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.
from .models import Cart, CartProduct, Order


class CartView(View):
    def get(self, request, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        cart_items = CartProduct.objects.filter(cart_id=cart_id)
        if len(cart_items) == 0:
            return render(request, 'cart.html', {'message': 'Empty basket.'})
        return render(request, 'cart.html', {'cart_items': cart_items, 'message': cart_id})


class DeleteFromCart(View):
    def post(self, request, pk):
        cart_product = CartProduct.objects.get(id=pk)
        cart_product.delete()
        return redirect(reverse('shopping_cart:cart', kwargs={'cart_id': cart_product.cart_id_id}))


class UserOrders(View):
    def get(self, request, **kwargs):
        user_id = self.kwargs.get('user_id')
        orders = Order.objects.filter(user_id=user_id)
        return render(request, 'user_orders.html', {'orders': orders})
