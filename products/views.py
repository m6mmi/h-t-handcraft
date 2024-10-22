from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, FormView
from random import shuffle

from h_t_handcraft import settings
from shopping_cart.models import Cart, CartProduct
from .forms import InquiryForm
from .models import Product, Category


class CategoryProductsView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        try:
            category = get_object_or_404(Category, id=self.kwargs.get('id'))
            return Product.objects.filter(category=category)
        except Exception as e:
            return Product.objects.none()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.META['HTTP_REFERER']

        return context


class IndexView(View):
    def get(self, request):
        products = list(Product.objects.all())
        shuffle(products)
        random_products = products[:8]

        return render(request, 'index.html', {'random_products': random_products})


class AddToCart(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart = Cart.objects.get_or_create(user_id=request.user.id, is_active=True)
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


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'terms_and_conditions.html'


class ProductSearchView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.none()


class CustomProductRequestView(SuccessMessageMixin, FormView):
    template_name = 'custom_product_request.html'
    form_class = InquiryForm
    success_url = reverse_lazy('products:thank_you')
    success_message = "Sinu soov on saadetud!"

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject_to_seller = f"Uus oma kirjeldusega toote soov"
        full_message_to_seller = f"Kiri on saadetud {name} ({email})poolt:\n\n{message} "
        send_mail(subject_to_seller, full_message_to_seller, settings.DEFAULT_FROM_EMAIL,
                  ['triinu.niklus@gmail.com'])

        subject_to_client = "H&T Käsitöö. Erilahendusega toode!"
        full_message_to_client = (f"{name},\n\nAitäh, me oleme kätte saanud sinu soovi erilahenduse kirjeldusega! "
                                  f"Keskmiselt vastame 1tööpäeva jooksul. \n\nSinu kirjeldus:\n{message}")
        send_mail(subject_to_client, full_message_to_client, settings.DEFAULT_FROM_EMAIL, [email])

        return super().form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'
