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


class StateView(APIView):
    def get(self, request):
        """Used to list all states, commented code for creating states"""
        # country = nigeria["name"]
        # country_instance = Country.objects.get(name=country)
        # for state in nigeria["states"]:
        #     State.objects.create(
        #         name=state["name"], state_code=state["state_code"], country=country_instance)
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CityView(APIView):
    def get(self, request):
        """Used to list all cities, commented code for creating cities"""
        # for state in nigeria["states"]:
        #     state_q = State.objects.get(name=state["name"])
        #     for city in state["cities"]:
        #         city_c = City.objects.create(name=city["name"], state=state_q)
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CountryStateView(APIView):
    def get(self, request, pk):
        try:
            country = Country.objects.get(id=pk)
        except Country.DoesNotExist:
            return Response({"message": "This country is not supported yet"}, status.HTTP_404_NOT_FOUND)
        country_states = country.country_states.all()
        serializer = StateSerializer(country_states, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class StateCityView(APIView):
    def get(self, request, pk):
        try:
            state = State.objects.get(id=pk)
        except State.DoesNotExist:
            return Response({"message": "This state does not exist or is not supported yet"}, status.HTTP_404_NOT_FOUND)
        cities = state.state_cities.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
