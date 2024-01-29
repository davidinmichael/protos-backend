from sys import exception
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
import ipinfo, os


def token_send_email(user_email, email_subject, template):
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=email_subject,
        body=template,
        from_email=from_email,
        to=to_email,
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
        print("Email sent to, ", user_email)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"Couldn't connect, please, try again"

    return None


ip_token = os.getenv("IPINFO_TOKEN")
def get_location():
    handler = ipinfo.getHandler(ip_token)
    try:
        details = handler.getDetails()
    except Exception as e:
        return "Couldn't get Location"
    data = {}
    data["latitude"] = details.latitude
    data["longitude"] = details.longitude
    return data
