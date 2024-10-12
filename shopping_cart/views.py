from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.models import Order, ShippingAddress
from .models import Cart, CartProduct


class UserOrders(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        orders = Order.objects.filter(user_id=self.request.user, cart__is_active=False)
        return render(request, 'user_orders.html', {'orders': orders})


class OrderView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        order_id = self.kwargs.get('id')
        cart_items = CartProduct.objects.filter(cart_id__order=order_id, cart__is_active=False).order_by('-id')
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))
        return render(request, 'order.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'order_id': order_id,
        })


class CartView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        cart_id = Cart.objects.filter(is_active=True, user=self.request.user).first()
        cart_items = CartProduct.objects.filter(cart=cart_id, cart__is_active=True).order_by('-id')
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))

        if not cart_items:
            return render(request, 'cart.html')
        return render(request, 'cart.html', {
                                                    'cart_items': cart_items,
                                                    'total_price': total_price
                                                })


class DeleteFromCart(View):
    def post(self, request, pk):
        cart_product = CartProduct.objects.get(id=pk)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        else:
            cart_product.delete()
        return redirect(request.META['HTTP_REFERER'])


class Checkout(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, 'checkout.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        county = request.POST.get('county')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')

        order = Order()
        order.cart = Cart.objects.get(user_id=self.request.user, is_active=True)
        order.user = self.request.user
        order.first_name = first_name
        order.last_name = last_name
        order.email = email
        order.address = address
        order.city = city
        order.county = county
        order.zipcode = zipcode
        order.country = country
        order.phone_number = phone_number
        order.save()

        return redirect(reverse('shopping_cart:shipping'))


class ShippingAddressView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, 'shipping.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        county = request.POST.get('county')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')

        shipping = ShippingAddress()
        shipping.order_id = Cart.objects.get(user_id=self.request.user, is_active=True).id
        shipping.user = self.request.user
        shipping.first_name = first_name
        shipping.last_name = last_name
        shipping.address = address
        shipping.city = city
        shipping.county = county
        shipping.zipcode = zipcode
        shipping.country = country
        shipping.phone_number = phone_number
        shipping.save()

        # CSet cart to inactive
        cart = Cart.objects.get(user_id=self.request.user, is_active=True)
        cart.is_active = False
        cart.save()

        return redirect(reverse('users:user_orders'))

