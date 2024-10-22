# Generated by Django 5.1.1 on 2024-10-20 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Itella',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.order')),
            ],
        ),
        migrations.CreateModel(
            name='Omniva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
