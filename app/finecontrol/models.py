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


class SyringeLoad_Db(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    volume = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class ZeroPosition_Db(models.Model):
    x = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    y = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

class PlateSizeSettings_Db(models.Model):
    x = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    y = models.DecimalField(decimal_places=2, max_digits=5, null=True)

class OffsetSettings_Db(models.Model):
    left = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    right = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    top = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    bottom = models.DecimalField(decimal_places=2, max_digits=5, null=False)

class Method_Db(models.Model):
    auth = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    filename = models.CharField(null=True, max_length=120)


class Application_Db(models.Model):
    method = models.ForeignKey(Method_Db, on_delete=models.CASCADE, null=False, blank=False)
    filename = models.CharField(null=False, blank=False, max_length=120)

    class Meta:
        abstract = True
