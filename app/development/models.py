from django.db import models
from django.contrib.auth import get_user_model
import finecontrol.models as core_models

class PlateProperties_Dev_Db(core_models.PlateProperties_Db):
    pass

class PressureSettings_Dev_Db(models.Model):
    pressure = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    temperature = models.DecimalField(null=True, decimal_places=2, max_digits=5, blank=True)
    nozzlediameter = models.CharField(max_length=120, default='0.08')
    speed = models.DecimalField(null=True, decimal_places=1, max_digits=5)

class BandSettings_Dev_Db(models.Model):
    volume = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    fluid = models.CharField(max_length=120, default='Methanol')
    printBothways = models.CharField(max_length=120, default='Off', blank=True)
    density = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    viscosity = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    applications = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)
    waitTime = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)
    description = models.CharField(max_length=120, default='', null=True, blank=True)


class Development_Db(models.Model):
    auth = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    filename = models.CharField(null=True, max_length=120)
    pressure_settings = models.OneToOneField(PressureSettings_Dev_Db, null=True, on_delete=models.CASCADE)
    plate_properties = models.ForeignKey(core_models.PlateProperties_Db, null=True, on_delete=models.CASCADE, blank=True)
    development_band_settings = models.OneToOneField(BandSettings_Dev_Db, null=True, on_delete=models.CASCADE)
    zero_position = models.ForeignKey(core_models.ZeroPosition, null=True, on_delete=models.CASCADE, blank=True)

class Flowrate_Db(models.Model):
    development_in_db = models.ForeignKey(
                Development_Db,
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    value = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
