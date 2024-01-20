from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


def token_send_email(user_email, email_subject, email_body, template):
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=email_subject,
        body=email_body,
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