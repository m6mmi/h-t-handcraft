# Generated by Django 5.1.1 on 2024-10-22 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_galleryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_path',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
