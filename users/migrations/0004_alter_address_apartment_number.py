# Generated by Django 5.1.1 on 2024-10-01 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='apartment_number',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
