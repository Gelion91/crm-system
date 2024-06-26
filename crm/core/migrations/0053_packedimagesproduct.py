# Generated by Django 4.2.7 on 2024-04-22 12:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_alter_imagesproduct_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackedImagesProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', validators=[django.core.validators.validate_image_file_extension])),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='packed_images', to='core.product')),
            ],
            options={
                'verbose_name': 'Изображение упакованного продукта',
                'verbose_name_plural': 'Изображения упакованного продукта',
                'ordering': ['-id'],
            },
        ),
    ]
