from django.db import models
from django.contrib.auth import get_user_model
# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters

class PlateProperties_Db(models.Model):
    size_x = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    size_y = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_left = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_right = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_top = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_bottom = models.DecimalField(decimal_places=2, max_digits=5, null=True)

class BandSettings_Db(models.Model):
    main_property = models.DecimalField(null=True,decimal_places=0, max_digits=6)
    value = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    height = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    gap = models.DecimalField(null=True, decimal_places=2, max_digits=5)

class MovementSettings_Db(models.Model):
    motor_speed = models.DecimalField(null=True, decimal_places=0, max_digits=5)
    delta_x = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    delta_y = models.DecimalField(null=True, decimal_places=2, max_digits=5)

class PressureSettings_Db(models.Model):
    pressure = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    frequency = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    temperature = models.DecimalField(null=True, decimal_places=2, max_digits=5, blank=True)
    nozzlediameter = models.CharField(max_length=120, default='0.08')

class SampleApplication_Db(models.Model):
    auth = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file_name = models.CharField(null=True, max_length=120)
    movement_settings = models.OneToOneField(MovementSettings_Db, null=True, on_delete=models.CASCADE)
    pressure_settings = models.OneToOneField(PressureSettings_Db, null=True, on_delete=models.CASCADE)
    plate_properties = models.OneToOneField(PlateProperties_Db, null=True, on_delete=models.CASCADE)
    band_settings = models.OneToOneField(BandSettings_Db, null=True, on_delete=models.CASCADE)

class BandsComponents_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db, on_delete=models.CASCADE, blank=True, null=True,)
    band_number = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
    description = models.CharField(null=True, max_length=120, blank=True)
    volume = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    type = models.CharField(null=True, max_length=120, blank=True)
    density = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    viscosity = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)

