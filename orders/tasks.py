from celery import task
from django.core.mail import message, send_mail
from .models import Order

"""@task
def order_created(order_id):
    send emails notifs upon an order
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed and order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'm_krub@aol.com', [order.email], fail_silently=False)

    return mail_sent"""