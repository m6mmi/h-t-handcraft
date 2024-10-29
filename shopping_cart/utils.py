from users.models import Order
from users.views import InvoiceView


def send_invoice_email(user):
    order = Order.objects.get(user_id=user, cart__is_active=True)
    print(order)
    invoice_view = InvoiceView()
    pdf_file_path = invoice_view.generate_pdf(order)
    invoice_view.send_order_confirmation(order, pdf_file_path)
