# Generated by Django 4.2.7 on 2024-03-24 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_clients_phone_alter_logistics_delivery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='margin',
            new_name='margin_product',
        ),
    ]
