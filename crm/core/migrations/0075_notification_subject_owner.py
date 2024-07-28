# Generated by Django 4.2.7 on 2024-07-23 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0074_logistics_last_updater'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='subject_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_owner', to=settings.AUTH_USER_MODEL, verbose_name='Создатель объекта'),
        ),
    ]
