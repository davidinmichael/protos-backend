from django.urls import path
from .views import *

urlpatterns = [
    path("currencies/", CurrencyView.as_view()),
]
