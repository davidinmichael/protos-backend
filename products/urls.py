from django.urls import path
from .views import *


urlpatterns = [
    path("product-categories/", ProductCategory.as_view()),
    path("business-products/", BusinessProductView.as_view()),
]

