from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.template.loader import render_to_string
from .utils import *


@receiver(post_save, sender=PersonalAccount)
def send_welcome_email(sender, instance, created, **kwargs):
    user_token = UserToken.objects.create(user=instance)
    context = {
        'name': instance.get_account_name(),
        "token": user_token
    }
    template = render_to_string("account/email_token.html", context)
    if created:
        try:
            token_send_email(instance.email, "Verify Email",
                             user_token, template)
            print("Email sent to", instance.email)
            print("This is the token:", user_token)
        except:
            return "Couldn't connect, try again"
