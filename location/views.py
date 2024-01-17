from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .nigeria import nigeria
from .models import *
from .serializers import *


class CurrencyView(APIView):
    def get(self, request):
        """Used to created currency for the set country"""
        # currency_c = Currency.objects.create(
        #     name=nigeria["currency_name"], currency_symbol=nigeria["currency_symbol"], currency=nigeria["currency"])
        currency = Currency.objects.all()
        serializer = CurrencySerializer(currency, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
