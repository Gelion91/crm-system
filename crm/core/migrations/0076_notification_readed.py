# Generated by Django 4.2.7 on 2024-07-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_notification_subject_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='readed',
            field=models.BooleanField(default=False),
        ),
    ]