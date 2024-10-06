from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(help_text='Product description', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image_path = models.ImageField(upload_to='products/img', blank=True, null=True)
    stock = models.IntegerField(default=0, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
