from django.shortcuts import render
from django.views import View

# Product list CBV (Class-Based View)

from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
