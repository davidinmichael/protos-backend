from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.conf import settings
import random
import requests


from .serializers import *
from .models import *
from .utils import *



class GoogleCallBack(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
    # Extract the authorization code from the request URL
        code = request.GET.get('code')

        if code:
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,  # Your Google OAuth2 client ID
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,  # Your Google OAuth2 client secret
                'redirect_uri': 'https://protosapp.pythonanywhere.com/account/google/callback',  # Must match the callback URL configured in your Google API credentials
                'grant_type': 'authorization_code',
            }

            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)

            if response.status_code == 200:
                access_token = response.json().get('access_token')

                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_response = requests.get(profile_endpoint, headers=headers)

                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        # Create new user with the user info
                        user = PersonalAccount.objects.create_user(first_name=profile_data["given_name"],
                                                                   last_name=profile_data["family_name"],
                                                                   email=profile_data["email"])
                        refresh = RefreshToken.for_user(user)
                        data['access'] = str(refresh.access_token)
                        data['refresh'] = str(refresh)
                        return Response(data, status.HTTP_201_CREATED)
                    else:
                        return JsonResponse({'error': 'Failed to fetch profile information from Google'}, status=profile_response.status_code)
                else:
                    return JsonResponse({'error': 'Access token not found in response'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to exchange authorization code for access token'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'Authorization code not found in request parameters'}, status=400)


class PersonalAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        accounts = PersonalAccount.objects.all()
        serializer = PersonalAccountSerializer(accounts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = PersonalAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
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
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        data = {}
        try:
            user = PersonalAccount.objects.get(email=email)
        except PersonalAccount.DoesNotExist:
            return Response({"error": "User does not exist"}, status.HTTP_400_BAD_REQUEST)
        if user.password == password:
            print("new-password entered", password)
            serializer = PersonalAccountSerializer(user)
            refresh = RefreshToken.for_user(user)
            data["message"] = "Login Successfull"
            data["user_details"] = serializer.data
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            return Response(data, status.HTTP_200_OK)
        else:
            print("new-password-error", password)
            return Response({'error': 'Wrong Password'}, status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful, login to continue.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error logging out: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = PersonalAccount.objects.get(email=email)
        except PersonalAccount.DoesNotExist:
            return Response({"message": "User with this email does not exist"},
                            status.HTTP_400_BAD_REQUEST)
        user_token = UserToken.objects.create(user=user)
        context = {
            'name': user.get_account_name(),
            "token": user_token.token
        }
        template = render_to_string(
            "account/email_token.html", context)
        token_send_email(user.email, "Password Reset",
                         template)
        return Response({"message": "A verification code has been sent to your email."})


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        try:
            user = PersonalAccount.objects.get(email=email)
            user_token = UserToken.objects.get(token=token)
        except UserToken.DoesNotExist:
            return Response({"message": "Invalid Token"}, status.HTTP_400_BAD_REQUEST)
        if user_token.user == user:
            if password == confirm_password:
                user.set_password(password)
                return Response({"message": "Password reset succesfully, continue to login."},
                                status.HTTP_200_OK)
            else:
                return Response({"message": "Passwords do not match"},
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid token"}, status.HTTP_400_BAD_REQUEST)


class BusinessAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {}
        business = BusinessAccount.objects.get(owner=request.user)
        serializer = BusinessAccountSerializer(business)
        data["business"] = serializer.data
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        serializer = BusinessAccountSerializer(
            data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            business = serializer.save()
            refresh = RefreshToken.for_user(business.owner)
            data["message"] = "Account created successfully"
            data["business"] = serializer.data
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            return Response(data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CategoryView(APIView):
    def get(self, request):
        categories = BusinessCategory.objects.all()
        serializer = BusinessCategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CategoryView(APIView):
    def get(self, request):
        categories = BusinessCategory.objects.all()
        serializer = BusinessCategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class BusinessListings(APIView):
    def get(self, request):
        data = {}
        user = request.user
        serializer = PersonalAccountSerializer(user)
        city_businesses = list(BusinessAccount.objects.filter(city=user.city))
        random.shuffle(city_businesses)
        city_businesses_serializer = BusinessAccountSerializer(city_businesses, many=True)

        data["city_businesses"] = city_businesses_serializer.data

        if city_businesses.count() < 50:
            state_businesses = list(BusinessAccount.objects.filter(
                state=user.state))
            random.shuffle(state_businesses)
            state_businesses_serializer = BusinessAccountSerializer(
                state_businesses, many=True)
            data["state_businesses"] = state_businesses_serializer.data

            if state_businesses.count() < 50:
                country_businesses = list(BusinessAccount.objects.filter(
                    country=user.country))
                random.shuffle(country_businesses)
                country_business_serializer = BusinessAccountSerializer(
                    country_businesses, many=True)
                data["country_businesses"] = country_business_serializer.data

        data["current_user"] = serializer.data
        return Response(data, status.HTTP_200_OK)


class BusinessListingsOther(APIView):
    permission_classes = [AllowAny]

    def get(self, request, location):
        try:
            businesses = BusinessAccount.objects.filter(state__name=location)
        except BusinessAccount.DoesNotExist:
            businesses = BusinessAccount.objects.all()
        serializer = BusinessAccountSerializer(businesses, many=True)
        return Response(serializer.data, status.HTTP_200_OK)