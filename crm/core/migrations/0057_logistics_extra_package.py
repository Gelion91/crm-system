# Generated by Django 4.2.7 on 2024-04-26 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_logistics_places_alter_logistics_insurance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistics',
            name='extra_package',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Примечание по упаковке'),
        ),
    ]