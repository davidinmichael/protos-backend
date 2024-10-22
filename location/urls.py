from django.urls import path
from .views import *

urlpatterns = [
    path("create-currency/", CreateCurrency.as_view()),
    path("create-country/", CreateCountry.as_view()),
    path("create-state/", CreateState.as_view()),
    path("create-city/", CreateCity.as_view()),

    path("currencies/", CurrencyView.as_view()),
    path("countries/", CountryView.as_view()),
    # path("states/", StateView.as_view()),
    # path("cities/", CityView.as_view()),

    path("states/<str:pk>/", CountryStateView.as_view()),
    path("cities/<str:pk>/", StateCityView.as_view()),
]
