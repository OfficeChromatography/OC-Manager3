from django.db import models
from django.contrib.auth import get_user_model
from sampleapp.models import PlateProperties_Db, MovementSettings_Db, PressureSettings_Db

class PlateProperties_Dev_Db(PlateProperties_Db):
    pass

class MovementSettings_Dev_Db(MovementSettings_Db):
    pass

class PressureSettings_Dev_Db(PressureSettings_Db):
    pass

class BandSettings_Dev_Db(models.Model):
    volume = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    printBothways = models.BooleanField()

class Development_Db(models.Model):
    auth = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file_name = models.CharField(null=True, max_length=120)
    movement_settings = models.OneToOneField(MovementSettings_Db, null=True, on_delete=models.CASCADE)
    pressure_settings = models.OneToOneField(PressureSettings_Db, null=True, on_delete=models.CASCADE)
    plate_properties = models.OneToOneField(PlateProperties_Db, null=True, on_delete=models.CASCADE)
    developmentband_settings = models.OneToOneField(BandSettings_Dev_Db, null=True, on_delete=models.CASCADE)
