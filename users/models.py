from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Address(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    county = models.CharField(max_length=25)
    country = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
