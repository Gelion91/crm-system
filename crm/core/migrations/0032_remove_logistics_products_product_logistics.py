# Generated by Django 4.2.7 on 2024-02-29 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_rename_order_logistics_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logistics',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='logistics',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivers', to='core.logistics', verbose_name='Товары'),
        ),
    ]
