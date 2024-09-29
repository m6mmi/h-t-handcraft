from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Product, Category, Subcategory


class CategoryProductsView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['id'])
        return Product.objects.filter(subcategory__category=category)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
