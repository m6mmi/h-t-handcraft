from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Address(models.Model):
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=5)
    apartment_number = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.street
