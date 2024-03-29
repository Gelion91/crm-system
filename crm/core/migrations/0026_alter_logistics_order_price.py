# Generated by Django 4.2.7 on 2024-02-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_remove_order_arrive_price_remove_order_weight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logistics',
            name='order_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Стоимость товаров в заказах ¥'),
        ),
    ]
