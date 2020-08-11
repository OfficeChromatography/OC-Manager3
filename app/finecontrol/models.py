from django.db import models
from django.contrib.auth import get_user_model

class GcodeFile(models.Model):
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    gcode = models.FileField(null=True)
    gcode_url = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

class CleaningProcess_Db(models.Model):
    user = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    start_frequency = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    stop_frequency = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    steps = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    pressure = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

class ZeroPosition(models.Model):
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    zero_x = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    zero_y = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
