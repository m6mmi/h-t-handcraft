# Generated by Django 5.1.1 on 2024-09-28 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0005_alter_cart_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
