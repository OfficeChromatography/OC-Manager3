from django.db import models
from django.contrib.auth import get_user_model
# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters

class PlateProperties_Db(models.Model):
    size_x = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    size_y = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    offset_x = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    offset_y = models.DecimalField(decimal_places=0, max_digits=6, null=True)

class BandSettings_Db(models.Model):
    main_property = models.DecimalField(null=True,decimal_places=0, max_digits=6)
    value = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    height = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    gap = models.DecimalField(null=True, decimal_places=0, max_digits=6)

class MovementSettings_Db(models.Model):
    motor_speed = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    delta_x = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    delta_y = models.DecimalField(null=True, decimal_places=0, max_digits=6)

class PressureSettings_Db(models.Model):
    pressure = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    frequency = models.DecimalField(null=True, decimal_places=0, max_digits=6)

class SampleApplication_Db(models.Model):
    auth = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file_name = models.CharField(null=True, max_length=120)
    movement_settings = models.OneToOneField(MovementSettings_Db, null=True, on_delete=models.CASCADE)
    pressure_settings = models.OneToOneField(PressureSettings_Db, null=True, on_delete=models.CASCADE)
    plate_properties = models.OneToOneField(PlateProperties_Db, null=True, on_delete=models.CASCADE)
    band_settings = models.OneToOneField(BandSettings_Db, null=True, on_delete=models.CASCADE)
