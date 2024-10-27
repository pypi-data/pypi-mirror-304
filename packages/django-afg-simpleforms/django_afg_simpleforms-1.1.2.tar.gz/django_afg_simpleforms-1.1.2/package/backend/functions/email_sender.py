import ssl

from django.core.mail import send_mail
from django.template.loader import render_to_string
from .. import models


def send_email(customer_id, order_id):
    try:
        customer = models.Customer.objects.get(pk=customer_id)
        order = models.Order.objects.get(pk=order_id)
        category = models.Category.objects.get(pk=order.category_id)

        subject = 'Заказ на сайте Dash-Am'

        html_message = render_to_string('base/email_template.html',
                                        {'customer_name': order.name,
                                         'date_ordered': order.date_ordered,
                                         'order_category': category})

        send_mail(subject, None, None, [customer.email], html_message=html_message)
    except ssl.SSLCertVerificationError as e:
        print(f"SSL Certificate Verification Error: {e}")