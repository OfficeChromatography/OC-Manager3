# Generated by Django 3.0.5 on 2020-06-16 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0017_pressuresettings_db_enable_temperature'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pressuresettings_db',
            old_name='enable_temperature',
            new_name='temperature_control',
        ),
    ]
