from django.urls import path
from .views import *


urlpatterns = [
    path("personal-account/", PersonalAccountView.as_view()),
    path("verify-email/", VerifyEmail.as_view()),
    path("login/", LoginView.as_view()),
    path("send-token/", SendToken.as_view()),
    path("reset-password/", ResetPassword.as_view()),

    path("business-account/", BusinessAccountView.as_view()),
]
