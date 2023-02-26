import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_to_customer(basket, order):
    """Sending Email with Python Thread"""
    context = {
        'order': order,
        'date': order.created.date().strftime('%d.%m.%Y'),
        'total': basket.get_total_price(),
        'basket': basket
    }
    subject = 'Замовлення в Сіль і Пательня'
    html_content = render_to_string('orders/email.html', context)
    text_content = strip_tags(html_content)
    thread = threading.Thread(
        target=email_sender,
        args=(
            subject,
            text_content,
            html_content,
            [order.email]
        )
    )
    thread.start()


def email_sender(subject, text_content, html_content, recipients):
    """Send an email with order details to the customer's email"""
    message = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        recipients
    )
    message.attach_alternative(html_content, 'text/html')
    message.send()
