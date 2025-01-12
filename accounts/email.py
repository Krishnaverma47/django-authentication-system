from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task

@shared_task
def SendEmail(subject, template_name, context, from_email, recipient_list):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return True
    except Exception as e:
        print(f"Getting error while sending email: {str(e)}")
        return False