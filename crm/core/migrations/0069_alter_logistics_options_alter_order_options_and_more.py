# Generated by Django 4.2.7 on 2024-07-03 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0068_product_date_create_product_date_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logistics',
            options={'ordering': ['-date_create'], 'verbose_name': 'Доставка', 'verbose_name_plural': 'Доставки'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_create'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_create'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(blank=True, verbose_name='Действие')),
                ('subject', models.CharField(max_length=100, verbose_name='Объект')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ['-date_create'],
            },
        ),
    ]
