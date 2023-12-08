# Generated by Django 4.2.7 on 2023-11-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_order_total_price_product_draft_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='full_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Общая цена'),
        ),
    ]
