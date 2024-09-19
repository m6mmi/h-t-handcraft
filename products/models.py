# Lisatud 19.09.24

from django.db import models


class Subcategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(help_text='Product description')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(default=0, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
