# Generated by Django 4.2.7 on 2024-01-28 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_order_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fraht',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Стоимость доставки по Китаю ¥'),
        ),
        migrations.AlterField(
            model_name='product',
            name='full_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Общая цена ¥'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Цена ¥'),
        ),
        migrations.CreateModel(
            name='ImagesProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
                'ordering': ['-id'],
            },
        ),
    ]
