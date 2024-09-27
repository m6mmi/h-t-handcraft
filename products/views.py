from django.shortcuts import render
from django.views import View

# Product list CBV (Class-Based View)

from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  # Tepliit
    context_object_name = 'products'  # Templiidis kasutatud konteksti nimi
    paginate_by = 10  # Optional: Tooteid leheküljel

    def get_queryset(self):
        # Customize the queryset if necessary (e.g., filtering, ordering)
        return Product.objects.filter(stock__gt=0).order_by('-id')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'  # Templiit
    context_object_name = 'product'


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
