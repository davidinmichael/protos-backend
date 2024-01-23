from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string

from .serializers import *
from .models import *
from .utils import *


class PersonalAccountView(APIView):
    def post(self, request):
        serializer = PersonalAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            if user.is_business_owner:
                user_token = UserToken.objects.create(user=user)
                context = {
                    'name': user.get_account_name(),
                    "token": user_token.token
                }
                template = render_to_string(
                    "account/welcome_email.html", context)
                token_send_email(user.email, "Verify Email",
                                 user_token.token, template)
            else:
                data["name"] = f"Hello {user.first_name},"
                data["message"] = "Your Account is created successfully. Continue to Login"
            return Response(data, status.HTTP_201_CREATED)
        else:
            return (serializer.errors, status.HTTP_403_FORBIDDEN)


class VerifyEmail(APIView):
    def post(self, request):
        token = request.data.get("token")
        user = request.user
        try:
            user_token = UserToken.objects.get(token=token)
        except UserToken.DoesNotExist:
            return Response({"message": "Invalid Token"}, status.HTTP_400_BAD_REQUEST)
        if user_token.user == user:
            user.email_verified = True
            user.save()
            user_token.delete()
        return Response({"message": "Account Verified"}, status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        data = {}
        try:
            user = PersonalAccount.objects.get(email=email)
        except PersonalAccount.DoesNotExist:
            return Response({'error': 'User does not exist'}, status.HTTP_400_BAD_REQUEST)
        if user.check_password(password):
            serializer = PersonalAccountSerializer(user)
            refresh = RefreshToken.for_user(user)
            data["message"] = "Login Successfull"
            data["user_details"] = serializer.data
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            return Response(data, status.HTTP_200_OK)
        else:
            return Response({'error': 'Wrong Password'}, status.HTTP_400_BAD_REQUEST)


class BusinessAccountView(APIView):
    def post(self, request):
        serializer = BusinessAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["message"] = "Account created successfully"
            data["business"] = serializer.data
            return Response(data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class BusinessListings(APIView):
    def get(self, request):
        data = {}
        user = request.user
        user_details = PersonalAccount.objects.get(email=request.user.email)
        serializer = PersonalAccountSerializer(user_details)
        city_businesses = BusinessAccount.objects.filter(city=user.city.name)
        city_businesses_serializer = BusinessHourSerializer(
            city_businesses, many=True)
        data["city_businesses"] = city_businesses_serializer.data

        if city_businesses.count() < 50:
            state_businesses = BusinessAccount.objects.filter(
                state=user.state.name)
            state_businesses_serializer = BusinessHourSerializer(
                state_businesses, many=True)
            data["state_businesses"] = state_businesses_serializer.data

            if state_businesses.count() < 50:
                country_businesses = BusinessAccount.objects.filter(
                    country=user.country.name)
                country_business_serializer = BusinessHourSerializer(
                    country_businesses, many=True)
                data["country_businesses"] = country_business_serializer.data

        data["current_user"] = serializer.data
        return Response(data, status.HTTP_200_OK)
