# Generated by Django 4.2.7 on 2023-12-12 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_order_total_price_rub_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='result',
            field=models.BooleanField(default=False, verbose_name='Выполнен'),
        ),
    ]
