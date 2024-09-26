from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import Cart, CartProduct, Order


class CartView(View):
    def get(self, request, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        cart_items = CartProduct.objects.filter(cart_id=cart_id)
        print(len(cart_items))
        if len(cart_items) == 0:
            return render(request, 'cart.html', {'message': 'Empty basket.'})
        return render(request, 'cart.html', {'cart_items': cart_items, 'message': cart_id})
