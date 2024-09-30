from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Address(models.Model):
    address = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    zipcode = models.CharField(max_length=10, blank=False)
    county = models.CharField(max_length=25, blank=False)
    country = models.CharField(max_length=50, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
