import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_to_corporate_mail(form):
    """If form is valid send email with message to admin email"""
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    title = form.cleaned_data['title']
    message = form.cleaned_data['message']

    context = {
        'name': name,
        'email': email,
        'title': title,
        'message': message
    }
    subject = 'Побажання від клієнта'
    html_content = render_to_string('contacts/email.html', context)
    text_content = strip_tags(html_content)
    thread = threading.Thread(
        target=email_sender,
        args=(
            subject,
            text_content,
            html_content,
            [settings.EMAIL_HOST_USER]
        )
    )
    thread.start()


def email_sender(subject, text_content, html_content, recipients):
    """Send an email with message from customer to EMAIL_HOST_USER (corporate email)"""
    message = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        recipients
    )
    message.attach_alternative(html_content, 'text/html')
    message.send()
