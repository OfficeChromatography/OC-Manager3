# Generated by Django 3.0.5 on 2020-06-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0016_auto_20200616_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressuresettings_db',
            name='enable_temperature',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]