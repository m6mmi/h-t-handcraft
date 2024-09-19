from django.shortcuts import render

# Product list CBV (Class-Based View)

from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  # Tepliit
    context_object_name = 'products'  # Templiidis kasutatud konteksti nimi
    paginate_by = 10  # Optional: Tooteid leheküljel

    def get_queryset(self):
        # Customize the queryset if necessary (e.g., filtering, ordering)
        return Product.objects.filter(stock__gt=0).order_by('-id')

from django.views.generic import DetailView
from .models import Product # Kas on vaja korduvalt lisada?

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'  # Templiit
    context_object_name = 'product'