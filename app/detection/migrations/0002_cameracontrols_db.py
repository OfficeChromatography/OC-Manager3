# Generated by Django 3.0.5 on 2020-06-23 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraControls_Db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_exposure', models.CharField(blank=True, choices=[('0', 'off'), ('1', 'auto')], max_length=255, null=True)),
                ('exposure_dynamic_framerate', models.BooleanField(blank=True, null=True)),
                ('auto_exposure_bias', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('exposure_time_absolute', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('white_balance_auto_preset', models.CharField(blank=True, choices=[('0', 'off'), ('1', 'auto'), ('2', 'sunlight'), ('3', 'cloudy'), ('4', 'shade'), ('5', 'tungsten'), ('6', 'fluorescent'), ('7', 'incandescent'), ('8', 'flash'), ('9', 'horizon')], max_length=255, null=True)),
                ('image_stabilization', models.BooleanField(blank=True, null=True)),
                ('iso_sensitivity', models.CharField(blank=True, choices=[(0, 0), (1, 100000), (2, 200000), (3, 400000), (4, 900000)], max_length=255, null=True)),
                ('iso_sensitivity_auto', models.CharField(blank=True, choices=[(0, 'Manual'), (1, 'Auto')], max_length=255, null=True)),
                ('exposure_metering_mode', models.CharField(blank=True, choices=[(0, 'Averange'), (1, 'Center Weighted'), (2, 'Averange')], max_length=255, null=True)),
                ('scene_mode', models.CharField(blank=True, choices=[(0, 'None'), (8, 'Night'), (11, 'Sports')], max_length=255, null=True)),
            ],
        ),
    ]