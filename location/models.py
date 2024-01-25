from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} | {self.currency_symbol}"


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capital = models.CharField(max_length=50)
    phone_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name="country_currencies")
    iso2 = models.CharField(max_length=3, unique=True)
    iso3 = models.CharField(max_length=4, unique=True)
    flag = models.SlugField(max_length=50, null=True, blank=True)

    def generate_flag_url(self):
        return f"https://flagcdn.com/256x192/{self.iso2.lower()}.png"

    def save(self, *args, **kwargs):
        if not self.flag:
            self.flag = self.generate_flag_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.capital}"


class State(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    identifier = models.CharField(max_length=10, null=True, blank=True)
    state_code = models.CharField(
        max_length=5, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="country_states")

    def __str__(self):
        return f"{self.name} State of {self.country}"


class City(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="state_cities")

    def __str__(self):
        return f"{self.name} City of {self.state}"
