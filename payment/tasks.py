from io import BytesIO
import weasyprint
from celery import task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import  EmailMessage
from orders.models import Order

@task
def payment_completed(order_id):
    """
    send automatic emails notifs upon a successful payment
    """
    order = Order.objects.get(id=order_id)
    subject = f'Nduggabi - EE Invoice no: {order.id}'
    message = f'Thank you for your recent purchase at Nduggabi site. '\
                'Please do come back again soon!. ' \
                'Attached with this email is your receipt in pdf. '\
                'Please download for your own safekeeping.'
    email = EmailMessage(subject, message, 'm_krub@aol.com', [order.email])

    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()