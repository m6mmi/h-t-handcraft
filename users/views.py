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
            # Set up file path
            filename = f'Arve_{order.id}.pdf'
            filepath = os.path.join(settings.INVOICE_PATH, filename)

            # Create document and elements
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Define footer function
            def add_footer(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica", 9)
                footer_text = "Pank: [Panga nimi] | Pangakonto: [IBAN] | Saaja: [pangakonto omanik]"
                seller_info = "Müüja nimi: H&T Käsitöö | Telefon: +372 53304239 | E-post: kunst.on.moes@online.ee"
                canvas.drawString(2 * cm, 2 * cm, footer_text)
                canvas.drawString(2 * cm, 1.5 * cm, seller_info)
                canvas.restoreState()

            # Add logo and invoice info in one row
            logo_path = './templates/static/img/logo_no_background.png'
            try:
                logo = Image(logo_path, width=3.5 * cm, height=3 * cm, hAlign='LEFT')
            except Exception as e:
                raise ValueError(f"Logo laadimise viga: {e}")

            # Calculate payment due date (3 days from order date)
            payment_due_date = order.date_ordered + timedelta(days=3)

            # Prepare customer and invoice info
            invoice_info = f"""
            <b>Tellija:</b> {order.first_name} {order.last_name}<br/>
            <b>Arve nr:</b> {order.id}<br/>
            <b>Kuupäev:</b> {order.date_ordered.strftime("%d.%m.%Y")}<br/>
            <b>Maksetähtaeg:</b> {payment_due_date.strftime("%d.%m.%Y")}<br/>
            """
            shipping_info = "Tarneviis: "
            if hasattr(order, 'shippingaddress'):
                shipping_info += "DPD Kuller"
            elif hasattr(order, 'itella'):
                shipping_info += f"Itella ({order.itella.box_name})"
            elif hasattr(order, 'omniva'):
                shipping_info += f"Omniva ({order.omniva.box_name})"
            else:
                shipping_info += "Puudub"
            invoice_info += f"<b>{shipping_info}</b>"

            # Create table with logo and invoice info
            header_table = Table(
                [[logo, Paragraph(invoice_info, styles["Normal"])]],
                colWidths=[5 * cm, 12 * cm]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 3 * cm))

            # Table of items with headers
            data = [[
                Paragraph("Kirjeldus", styles["Normal"]),
                "Kogus",
                "Hind",
                "Summa"
            ]]
            total_sum = 0

            # Populate table data
            for cart_product in CartProduct.objects.filter(cart=order.cart):
                summa = cart_product.quantity * Decimal(cart_product.product.price)
                data.append([
                    Paragraph(cart_product.product.description, styles["Normal"]),  # Wrap text
                    cart_product.quantity,
                    f"{cart_product.product.price:.2f} EUR",
                    f"{summa:.2f} EUR"
                ])
                total_sum += summa

            # Add total row
            data.append(["", "", "Kokku", f"{total_sum:.2f} EUR"])

            # Create and style table
            table = Table(data, colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),
            ]))
            elements.append(table)

            # Build the document
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
