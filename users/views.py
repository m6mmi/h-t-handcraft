import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from h_t_handcraft import settings
from shopping_cart.models import CartProduct
from .forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import User, Order, Feedback
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('users:profile')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"User logged in: {user.username}")

            return redirect('users:profile')
        else:
            print(form.errors)
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:profile')
    template_name = 'change_password.html'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user, cart__is_active=False).order_by('-id')[:5]
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class FeedbackView(View):
    def get(self, request):
        return render(request, 'feedback.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Feedback.objects.create(name=name, email=email, message=message)

        messages.success(request, 'Thank you for your feedback!')
        return redirect('users:feedback_list')


class FeedbackListView(View):
    def get(self, request):
        feedbacks = Feedback.objects.all().order_by('-created_at')
        return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


class InvoiceView(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponse("Tellimust ei leitud", status=404)

        pdf_file_path = self.generate_pdf(order)
        if pdf_file_path:
            self.send_order_confirmation(order, pdf_file_path)

            with open(pdf_file_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Arve_{order.id}.pdf"'
                return response
        else:
            return HttpResponse("Arve genereerimine ebaõnnestus", status=500)

    def generate_pdf(self, order):
        try:
            filename = f'Arve_{order.id}.pdf'
            filepath = os.path.join(settings.INVOICE_PATH, filename)

            # PDF loomine
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Logo
            logo_path = os.path.join(settings.STATIC_ROOT, 'logo.png')
            elements.append(Spacer(1, 12))
            elements.append(Image(logo_path, width=200, height=100))
            elements.append(Spacer(1, 12))

            # Pealkiri
            title = Paragraph(f'Tellimus nr: {order.id}', styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))

            # Kasutaja info
            user_info = Paragraph(f'Kasutajanimi: {order.user.username}', styles['Normal'])
            elements.append(user_info)
            elements.append(Spacer(1, 12))
            date_info = Paragraph(f'Kuupäev: {order.date_ordered.strftime("%d-%m-%Y")}', styles['Normal'])
            elements.append(date_info)
            elements.append(Spacer(1, 12))
            cart_id_info = Paragraph(f'Cart ID: {order.cart.id}', styles['Normal'])
            elements.append(cart_id_info)
            elements.append(Spacer(1, 12))

            elements.append(Paragraph('Teie tellimuses on järgmised tooted:', styles['Normal']))
            elements.append(Spacer(1, 12))

            # Lisame tooteinfo tabelina
            data = [["Toode", "Kogus", "Hind"]]
            for cart_product in CartProduct.objects.filter(cart=order.cart):
                data.append([cart_product.product.title, cart_product.quantity, f"{cart_product.product.price} EUR"])

            # Tabeli loomine
            table = Table(data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)
            elements.append(table)

            # Kokkuvõtte
            total_amount = sum(cart_product.quantity * cart_product.product.price for cart_product in
                               CartProduct.objects.filter(cart=order.cart))
            total_info = Paragraph(f'Kokku: {total_amount} EUR', styles['Normal'])
            elements.append(total_info)

            doc.build(elements)

            print(f"PDF genereeritud: {filepath}")
            return filepath
        except Exception as e:
            print(f"Ei saanud PDF genereerida: {e}")
            return None

    def send_order_confirmation(self, order, pdf_file):
        if not pdf_file:
            print("PDF-fail, mida lisada puudub.")
            return

        subject = f'Tellimuse kinnitus #{order.id}'

        html_content = f"""
        <p>Tere, {order.user.first_name}!</p>
        <p>Aitäh, et tellisite! Siin on teie tellimuse andmed:</p>
        <ul>
            <li><strong>Tellimuse number:</strong> {order.id}</li>
            <li><strong>Tellimuse kuupäev:</strong> {order.date_ordered.strftime('%d-%m-%Y')}</li>
        </ul>
        <p>Külastage meid jälle!</p>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )
        email.attach_alternative(html_content, "text/html")

        try:
            email.attach_file(pdf_file)
            email.send()
            print(f"E-kiri saadetud {order.user.email} koos arvega {pdf_file}.")
        except Exception as e:
            print(f"Ei saanud saata e-kirja: {e}")
