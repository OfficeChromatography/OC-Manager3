from django.db import models
from django.contrib.auth import get_user_model
from sampleapp.models import PlateProperties_Db
from finecontrol.models import ZeroPosition

class PlateProperties_Dev_Db(PlateProperties_Db):
    pass

class PressureSettings_Dev_Db(models.Model):
    pressure = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    temperature = models.DecimalField(null=True, decimal_places=2, max_digits=5, blank=True)
    nozzlediameter = models.CharField(max_length=120, default='0.08')

class BandSettings_Dev_Db(models.Model):
    volume = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    fluid = models.CharField(max_length=120, default='Methanol')
    printBothways = models.CharField(max_length=120, default='Off')
    density = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    viscosity = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    applications = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)
    precision = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)
    waitTime = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)

class Development_Db(models.Model):
    auth = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file_name = models.CharField(null=True, max_length=120)
    pressure_settings = models.OneToOneField(PressureSettings_Dev_Db, null=True, on_delete=models.CASCADE)
    plate_properties = models.OneToOneField(PlateProperties_Db, null=True, on_delete=models.CASCADE)
    developmentBandSettings = models.OneToOneField(BandSettings_Dev_Db, null=True, on_delete=models.CASCADE)
    zero_position = models.OneToOneField(ZeroPosition, null=True, on_delete=models.CASCADE)
