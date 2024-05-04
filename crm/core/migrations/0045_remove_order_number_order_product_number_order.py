# Generated by Django 4.2.7 on 2024-03-27 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_order_number_order_alter_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='number_order',
        ),
        migrations.AddField(
            model_name='product',
            name='number_order',
            field=models.CharField(blank=True, max_length=100, verbose_name='Номер заказа'),
        ),
    ]