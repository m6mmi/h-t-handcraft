# Generated by Django 5.1.1 on 2024-09-28 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0002_alter_cart_user_id_alter_order_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='active',
        ),
        migrations.AddField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]