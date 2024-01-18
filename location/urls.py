from django.urls import path
from .views import *

urlpatterns = [
    path("currencies/", CurrencyView.as_view()),
    path("countries/", CountryView.as_view()),
    path("states/", StateView.as_view()),
]
