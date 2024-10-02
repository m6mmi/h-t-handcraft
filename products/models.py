# Lisatud 19.09.24

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(help_text='Product description', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(default=0, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
