from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from shopping_cart.models import Cart, CartProduct
from .models import Product, Category


class CategoryProductsView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # TODO add try exception handling
        category = get_object_or_404(Category, id=self.kwargs.get('id'))
        return Product.objects.filter(subcategory__category=category)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class AddToCart(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart = Cart.objects.get_or_create(user_id=request.user.id, is_active=True)
        print(cart)
        cart_product, created = CartProduct.objects.get_or_create(product_id=product.id, cart=cart[0])
        if created:
            cart_product.quantity = 1
        else:
            if product.stock > cart_product.quantity:
                cart_product.quantity += 1
            else:
                return redirect(request.META['HTTP_REFERER'])
        cart_product.save()

        return redirect(request.META['HTTP_REFERER'])
