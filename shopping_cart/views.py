from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from users.models import Address
from .models import Cart, CartProduct, Order


class UserOrders(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        orders = Order.objects.filter(user_id=self.request.user, cart__is_active=False)
        print(orders)
        return render(request, 'user_orders.html', {'orders': orders})


class OrderView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        cart_items = CartProduct.objects.filter(cart_id=cart_id)
        try:
            cart = get_object_or_404(Cart, cart_id=cart_id)
        except Http404:
            return redirect(reverse('index'))
        if cart.is_active:
            return redirect(reverse('index'))
        return render(request, 'order.html', {'cart_items': cart_items})


class CartView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        cart_id = Cart.objects.filter(is_active=True, user_id=self.request.user).first()
        cart_items = CartProduct.objects.filter(cart_id=cart_id, cart_id__is_active=True)
        return render(request, 'cart.html', {'cart_items': cart_items})


class DeleteFromCart(View):
    def post(self, request, pk):
        cart_product = CartProduct.objects.get(id=pk)
        cart_product.delete()
        return redirect(reverse('shopping_cart:cart', kwargs={'cart_id': cart_product.cart_id_id}))


class Checkout(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user_id = self.request.user
        contact = Address.objects.get(user_id=user_id)

        return render(request, 'checkout.html',
                      {'user_id': user_id, 'contact': contact})
