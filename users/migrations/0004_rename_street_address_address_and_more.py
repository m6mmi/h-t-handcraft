# Generated by Django 5.1.1 on 2024-09-29 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='street',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='apartment_number',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='house_number',
            new_name='zipcode',
        ),
        migrations.RemoveField(
            model_name='address',
            name='postal_code',
        ),
        migrations.AddField(
            model_name='address',
            name='county',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
