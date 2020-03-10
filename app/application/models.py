from django.db import models
from django.contrib.auth import get_user_model
# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters

class PlateProperties_Db(models.Model):
    sizex = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    sizey = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    offsetx = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    offsety = models.DecimalField(decimal_places=0, max_digits=6, null=True)

class BandSettings_Db(models.Model):
    bandsetting = models.CharField(max_length=120, null=True)
    nbands = models.DecimalField(decimal_places=0, max_digits=6)
    lengthbands = models.DecimalField(decimal_places=0, max_digits=6)
    height = models.DecimalField(decimal_places=0, max_digits=6)
    gap = models.DecimalField(decimal_places=0, max_digits=6)

class SampleApplication_Db(models.Model):
    auth_id = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    filename = models.CharField(max_length=120, null=True)
    motorspeed = models.DecimalField(decimal_places=0, max_digits=6)
    pressure = models.DecimalField(decimal_places=0, max_digits=6)
    deltapressure = models.DecimalField(decimal_places=0, max_digits=6)
    plateproperties = models.OneToOneField(PlateProperties_Db, null=True, on_delete=models.CASCADE)
    bandsettings = models.OneToOneField(BandSettings_Db, null=True, on_delete=models.CASCADE)
