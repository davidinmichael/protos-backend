from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import uuid
from location.models import *


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        else:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PersonalAccount(AbstractUser):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(
        max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    is_business_owner = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.username}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).replace('-', "").upper()[:7]
        if not self.username:
            self.username = f"{self.first_name}{self.user_id}"
        return super().save(*args, **kwargs)

    def get_account_name(self):
        return f"{self.first_name} {self.last_name}"


class BusinessCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BusinessAccount(models.Model):
    owner = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.SET_NULL)
    postal_code = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    website = models.SlugField(
        unique=True, null=True, blank=True, max_length=100)
    categories = models.ManyToManyField(BusinessCategory, blank=True)
    business_id = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.owner} | {self.name}"

    def save(self, *args, **kwargs):
        if not self.owner.is_business_owner:
            self.owner.is_business_owner = True
            self.owner.save()
        if not self.business_id:
            self.business_id = str(uuid.uuid4()).replace('-', "").upper()[:7]
        return super().save(*args, **kwargs)


class UserToken(models.Model):
    user = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=7, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4()).replace('-', "").upper()[:4]
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.token


class BusinessHour(models.Model):
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, blank=True, null=True, related_name="business_hours")
    day = models.CharField(max_length=10, null=True, blank=True)
    open_time = models.CharField(
        max_length=10, null=True, blank=True)  # "09:00:00"
    close_time = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.business} | {self.open_time}"


class UserLocation(models.Model):
    user = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    def _str__(self):
        return f"{self.user} | {self.latitude}, {self.longitude}"

class BusinessLocation(models.Model):
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    def _str__(self):
        return f"{self.business} | {self.latitude}, {self.longitude}"

# {
#   "owner": {
#     "email": "dadvantech@gmail.com",
#     "password": "Front@1234",
#     "country": "Nigeria",
#     "state": "Abia",
#     "city": "Aba"
#   },
#   "categories": [
#     {"name": "Restaurant"},
#     {"name": "Bar"}
#     ],
#   "hours": [
#       {"day":"Monday", "open_time":"08:00 AM", "close_time":"17:00 PM"},
#       {"day":"Tuesday", "open_time":"08:00 AM", "close":"17:00 PM"},
#       {"day":"Wednessday", "open_time":"08:00 AM", "close":"17:00 PM"},
#       {"day":"Thursday", "open_time":"08:00 AM", "close":"17:00 PM"},
#       {"day":"Friday", "open_time":"08:00 AM", "close":"17:00 PM"}
#   ],
#   "country": "Nigeria",
#   "state": "Abia",
#   "city": "Aba",
#   "name": "iLight Wears",
#   "email": "ilghtwears@gmail.com",
#   "contact_number": "+2348140980792"
# }

