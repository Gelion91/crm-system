# Generated by Django 4.2.7 on 2024-03-17 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_order_margin_order_profit_product_margin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='marker',
            new_name='product_marker',
        ),
    ]
