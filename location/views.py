from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .nigeria import nigeria
from .models import *
from .serializers import *


class CurrencyView(APIView):
    def get(self, request):
        """Used to create currency for the set country"""
        # currency_c = Currency.objects.create(
        #     name=nigeria["currency_name"], currency_symbol=nigeria["currency_symbol"], currency=nigeria["currency"])
        currency = Currency.objects.all()
        serializer = CurrencySerializer(currency, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CountryView(APIView):
    def get(self, request):
        """Returns a list of all countries available in our database."""
        # currency_name = nigeria["currency_name"]
        # currency_instance = Currency.objects.filter(name=currency_name).first()

        # country_c = Country.objects.create(name=nigeria["name"], iso3=nigeria["iso3"], iso2=nigeria["iso2"],
        #                                    phone_code=nigeria["phone_code"], capital=nigeria["capital"], currency=currency_instance)
        country = Country.objects.all()
        serializer = CountrySerializer(country, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
