from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.
from .models import Cart, CartProduct, Order


class CartView(View):
    def get(self, request, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        cart_items = CartProduct.objects.filter(cart_id=cart_id)
        order = Order.objects.get(order_id=cart_id)
        if order.confirmation:
            order_confirmed = True
        else:
            order_confirmed = False
        if len(cart_items) == 0:
            return render(request, 'cart.html', {'message': 'Empty basket.'})
        return render(request, 'cart.html', {'cart_items': cart_items,
                                             'message': cart_id,
                                             'order_confirmed': order_confirmed})


class DeleteFromCart(View):
    def post(self, request, pk):
        cart_product = CartProduct.objects.get(id=pk)
        cart_product.delete()
        return redirect(reverse('shopping_cart:cart', kwargs={'cart_id': cart_product.cart_id_id}))


class UserOrders(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        orders = Order.objects.filter(user_id=self.request.user)
        return render(request, 'user_orders.html', {'orders': orders})
