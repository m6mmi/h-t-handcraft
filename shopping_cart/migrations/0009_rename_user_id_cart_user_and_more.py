# Generated by Django 5.1.1 on 2024-10-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0008_alter_cartproduct_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartproduct',
            old_name='cart_id',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartproduct',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cart_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='zipcode',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
