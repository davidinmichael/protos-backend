from email.policy import default
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
    date_joined = models.DateField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = AccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.username}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).replace('-', "").upper()[:7]
        return super().save(*args, **kwargs)