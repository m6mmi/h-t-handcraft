from random import shuffle

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation.trans_null import get_language
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, FormView

from h_t_handcraft import settings
from shopping_cart.models import Cart, CartProduct
from .forms import InquiryForm
from .models import Product, Category, GalleryImage


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
        image = form.cleaned_data.get('image')

        subject_to_seller = "Uus oma kirjeldusega toote soov"
        full_message_to_seller = f"Kiri on saadetud {name} ({email}) poolt:\n\n{message}"

        email_to_seller = EmailMessage(
            subject=subject_to_seller,
            body=full_message_to_seller,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['SELLER_EMAIL']
        )

        if image:
            email_to_seller.attach(image.name, image.read(), image.content_type)

        email_to_seller.send(fail_silently=False)

        subject_to_client = "H&T Käsitöö - Erilahendusega toode!"
        full_message_to_client = (f"{name},\n\nAitäh, me oleme kätte saanud sinu erilahenduse kirjelduse! "
                                  f"Keskmiselt vastame ühe tööpäeva jooksul. \n\nSinu kirjeldus:\n{message}")

        email_to_client = EmailMessage(
            subject=subject_to_client,
            body=full_message_to_client,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )

        email_to_client.send(fail_silently=False)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = GalleryImage.objects.all()
        return context


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'
