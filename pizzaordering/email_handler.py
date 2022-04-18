# setting email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string, get_template


def send_email(customer_email=None, order_data=None):
    # email_template = get_template("ordering_email.htm")
    # print(email_template)
    converted_template = render_to_string("ordering_email.htm", context={})
    email = EmailMessage(
        subject='subject',
        body=converted_template,
        from_email=settings.EMAIL_HOST_USER,
        to=["rojoto7086@1uscare.com"]
    )

    email.content_subtype = "html"
    email.fail_silently = False
    email.send()
