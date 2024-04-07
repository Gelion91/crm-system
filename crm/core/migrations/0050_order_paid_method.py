# Generated by Django 4.2.7 on 2024-04-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_order_total_price_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_method',
            field=models.CharField(choices=[('Альфа-банк', 'Альфа-банк'), ('Сбер', 'Сбер'), ('Тинькофф', 'Тинькофф'), ('Тимофеев', 'Тимофеев'), ('Наличные', 'Наличные'), ('Расчетный счет', 'Расчетный счет')], default='Наличные', max_length=100, verbose_name='Способ оплаты'),
        ),
    ]
