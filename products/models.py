from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(help_text='Product description', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    image_path = models.ImageField(upload_to='products/img', null=True, blank=True)
    stock = models.IntegerField(default=0, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # height = models.FloatField(null=True, blank=True)
    # width = models.FloatField(null=True, blank=True)
    # length = models.FloatField(null=True, blank=True)
    # weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        category_name = Category.objects.get(id=self.category.id)
        return f'{category_name} --- {self.title}, Laos: {self.stock}'


class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title
