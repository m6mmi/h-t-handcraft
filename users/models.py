import uuid

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=5)
    apartment_number = models.CharField(max_length=5)
    country = models.CharField(max_length=50)
    user_id = User.id

    def __str__(self):
        return self.street
