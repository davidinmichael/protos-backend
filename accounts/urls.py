from django.urls import path
from .views import *


urlpatterns = [
    path("personal-account/", PersonalAccountView.as_view()),
]
