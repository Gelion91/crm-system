# Generated by Django 4.2.7 on 2024-07-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_alter_logistics_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Курс $')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
        ),
    ]