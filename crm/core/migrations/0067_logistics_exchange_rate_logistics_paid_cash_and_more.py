# Generated by Django 4.2.7 on 2024-06-14 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_alter_notesproduct_options_notesdelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistics',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Курс $ на момент оплаты'),
        ),
        migrations.AddField(
            model_name='logistics',
            name='paid_cash',
            field=models.CharField(choices=[('Рубли', 'Рубли'), ('Доллары', 'Доллары')], default='ruble', max_length=100, verbose_name='Валюта оплаты'),
        ),
        migrations.AlterField(
            model_name='logistics',
            name='full_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Общая стоимость(Доставка/упаковка/страховка) $'),
        ),
    ]
