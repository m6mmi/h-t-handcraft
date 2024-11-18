import os
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from reportlab.lib.units import cm
from h_t_handcraft import settings
from shopping_cart.models import CartProduct
from .forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import User, Order, Feedback
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageTemplate
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
            # Määrame faili asukoha
            filename = f'Arve_{order.id}.pdf'
            filepath = os.path.join(settings.INVOICE_PATH, filename)

            # Loo PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Jaluse funktsioon
            def add_footer(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica", 9)

                # Jalus
                footer_data = [
                    [
                        "Tartumaa, Kastre vald\nKurepalu\nFIE Ragne Hanko",
                        "Telefon: +372 53304239\nE-post: kunst.on.moes@online.ee\nFacebook: H&T Käsitöö",
                        "Arvelduskonto nr\nEE204204278626434500\nRAGNE HANKO"
                    ]
                ]

                footer_table = Table(
                    footer_data,
                    colWidths=[5 * cm, 7 * cm, 5 * cm]
                )
                footer_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))

                width, height = A4
                footer_table.wrapOn(canvas, width, height)
                footer_table.drawOn(canvas, 2 * cm, 1 * cm)

                canvas.restoreState()

            # Logo
            logo_path = './templates/static/img/logo_no_2.png'
            try:
                logo = Image(logo_path, width=3.5 * cm, height=3 * cm, hAlign='LEFT')
            except Exception as e:
                raise ValueError(f"Logo laadimise viga: {e}")

            # Pealkiri
            invoice_title = Paragraph(f"<b>ARVE NR {order.id}</b>", styles["Title"])

            # Logo ja pealkirja paigutus
            header_row = Table(
                [
                    [logo, invoice_title]
                ],
                colWidths=[4 * cm, 12 * cm]
            )
            header_row.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(header_row)
            elements.append(Spacer(1, 0.5 * cm))

            # Maksetähtaeg
            payment_due_date = order.date_ordered + timedelta(days=3)

            # Saaja
            recipient_info = f"""
            <b>Tellija:</b> {order.first_name} {order.last_name}<br/>
            <b>Tellija kontakt:</b> {order.phone_number}<br/>
            <b>Kuupäev:</b> {order.date_ordered.strftime("%d.%m.%Y")}<br/>
            <b>Maksetähtaeg:</b> {payment_due_date.strftime("%d.%m.%Y")}<br/>
            """

            # Saatja
            sender_info = f"""
            <b>Saatja:</b> FIE Ragne Hanko<br/>
            <b>Registrikood:</b> 14460580<br/>
            """

            # Saaja ja saatja andmete paigutus
            info_table = Table(
                [
                    [Paragraph(recipient_info, styles["Normal"]), Paragraph(sender_info, styles["Normal"])]
                ],
                colWidths=[10 * cm, 6 * cm]
            )
            info_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 2 * cm))

            # Kirjelduste tabeli päis
            data = [[
                Paragraph("Kirjeldus", styles["Normal"]),
                "Kogus",
                "Hind",
                "Summa"
            ]]
            total_sum = 0

            # Tabeli sisu
            for cart_product in CartProduct.objects.filter(cart=order.cart):
                summa = cart_product.quantity * Decimal(cart_product.product.price)
                data.append([
                    Paragraph(cart_product.product.description, styles["Normal"]),
                    cart_product.quantity,
                    f"{cart_product.product.price:.2f} EUR",
                    f"{summa:.2f} EUR"
                ])
                total_sum += summa

            # Kokkuvõtte rida
            data.append(["", "", "Kokku", f"{total_sum:.2f} EUR"])

            # Loome ja kujundame tabeli
            table = Table(data, colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),
            ]))
            elements.append(table)

            # PDF genereerimine
            doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
            return filepath

        except Exception as e:
            raise ValueError(f"Ei saanud PDF genereerida: {e}")

    def send_order_confirmation(self, order, pdf_file):
        if not pdf_file:
            print("PDF-fail, mida lisada puudub.")
            return

        subject = f'Tellimuse kinnitus #{order.id}'

        html_content = f"""
        <p>Tere, {order.first_name}!</p>
        <p>Aitäh, et tellisite!</p>
        <p>Oleme Teie tellimuse kätte saanud. Kui olete arve tasunud paneme paki 3 tööpäeva jooksul teele.</p>
        <p>Siin on teie tellimuse andmed:</p>
        <ul>
            <li><strong>Tellimuse number:</strong> {order.id}</li>
            <li><strong>Tellimuse kuupäev:</strong> {order.date_ordered.strftime('%d-%m-%Y')}</li>
        </ul>
        <p>Ootame Teid jälle ostlema!</p>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
            cc=[settings.SELLER_EMAIL],
        )
        email.attach_alternative(html_content, "text/html")

        try:
            email.attach_file(pdf_file)
            email.send()
            print(f"E-kiri saadetud {order.user.email} koos arvega {pdf_file}.")
        except Exception as e:
            print(f"Ei saanud saata e-kirja: {e}")
