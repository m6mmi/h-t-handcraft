import os
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
            # Step 1: Set up file path
            filename = f'Arve_{order.id}.pdf'
            filepath = os.path.join(settings.INVOICE_PATH, filename)
            print(f"Filepath set to: {filepath}")

            # Step 2: Create the document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []
            print("Document and stylesheet initialized.")

            # Step 3: Add footer template
            def add_footer(canvas, doc):
                try:
                    print("Adding footer...")
                    canvas.saveState()
                    footer_text = "Panga nimi: [Panga nimi] | Pangakonto number: [Pangakonto IBAN]"
                    canvas.setFont("Helvetica", 10)
                    canvas.drawString(2 * cm, 1 * cm, footer_text)  # 2 cm from left, 1 cm from bottom
                    canvas.restoreState()
                    print("Footer added successfully.")
                except Exception as e:
                    print(f"Error in add_footer: {e}")
                    raise

            try:
                doc.build(elements)
            except Exception as e:
                print(f"Error during doc.build: {e}")

            doc.addPageTemplates([PageTemplate(id='FooterTemplate', onPage=add_footer)])
            print("Footer template added.")

            # Step 4: Add logo
            logo_path = './templates/static/img/logo.png'
            print(f"Logo path using Django static files: {logo_path}")
            elements.append(Spacer(1, 0.5 * cm))
            elements.append(Image(logo_path, width=5 * cm, height=2.5 * cm))
            elements.append(Spacer(1, 0.5 * cm))
            print("Logo added using Django static helper.")

            # Step 5: Add title and date
            elements.append(Paragraph(f'Arve nr: {order.id}', styles['Title']))
            elements.append(Spacer(1, 0.5 * cm))
            elements.append(Paragraph(f'Kuupäev: {order.date_ordered.strftime("%d-%m-%Y")}', styles['Normal']))
            elements.append(Spacer(1, 1 * cm))
            print("Title and date added.")

            # Step 6: Create table data
            data = [["Kirjeldus", "Kogus", "Hind", "Summa"]]
            print("Starting to populate table data...")
            for cart_product in CartProduct.objects.filter(cart=order.cart):
                summa = cart_product.quantity * Decimal(cart_product.product.price)
                data.append([
                    cart_product.product.description,
                    cart_product.quantity,
                    f"{cart_product.product.price:.2f} EUR",
                    f"{summa:.2f} EUR"
                ])
            print("Table data populated:", data)

            # Step 7: Style the table
            table = Table(data, colWidths=[5 * cm, 3 * cm, 3 * cm, 3 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(table)
            print("Table styled and added to elements.")

            # Step 8: Build the document
            doc.build(elements)
            print(f"PDF successfully generated: {filepath}")
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
