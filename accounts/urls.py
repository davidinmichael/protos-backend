from django.urls import path
from .views import *


urlpatterns = [
    path("google-signup/", GoogleAuthRedirect.as_view()),
    path("google/callback/", GoogleCallBack.as_view()),
    path("personal-account/", PersonalAccountView.as_view()),
    path("verify-email/", VerifyEmail.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("send-token/", SendToken.as_view()),
    path("reset-password/", ResetPassword.as_view()),

    path("categories/", CategoryView.as_view()),
    path("business-account/", BusinessAccountView.as_view()),
    path("business-listings/", BusinessListings.as_view()),
    path("business-listings-others/<str:location>/", BusinessListingsOther.as_view()),
]
