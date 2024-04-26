# Generated by Django 4.2.7 on 2024-04-23 14:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_packedimagesproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistics',
            name='first_step',
            field=models.BooleanField(default=False, verbose_name='Отправлен'),
        ),
        migrations.AddField(
            model_name='logistics',
            name='second_step',
            field=models.BooleanField(default=False, verbose_name='В Москве'),
        ),
        migrations.AddField(
            model_name='logistics',
            name='third_step',
            field=models.BooleanField(default=False, verbose_name='Получен клиентом'),
        ),
        migrations.AlterField(
            model_name='packedimagesproduct',
            name='image',
            field=models.ImageField(upload_to='packed_images/', validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
