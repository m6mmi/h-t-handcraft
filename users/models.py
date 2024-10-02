from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    zipcode = models.CharField(max_length=10, blank=False)
    county = models.CharField(max_length=25, blank=False)
    country = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
