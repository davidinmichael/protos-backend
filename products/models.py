from django.db import models
from accounts.models import BusinessAccount, PersonalAccount


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BusinessProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=30, decimal_places=4)
    category = models.ForeignKey(ProductCategory, null=True,
                                 blank=True, on_delete=models.CASCADE)
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    owner = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='products/', null=True,
                                blank=True, default="default-product.jpg")

    def __str__(self):
        return f"{self.name} - {self.price} | {self.business.name}"
