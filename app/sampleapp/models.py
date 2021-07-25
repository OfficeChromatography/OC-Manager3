from django.db import models
import finecontrol.models as core_models


class BandSettings_Db(models.Model):
    main_property = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    value = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    height = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    gap = models.DecimalField(null=True, decimal_places=2, max_digits=5)


class ApplicationSettings_Db(models.Model):
    motor_speed = models.DecimalField(null=True, decimal_places=0, max_digits=5)
    pressure = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    frequency = models.DecimalField(null=True, decimal_places=1, max_digits=5)
    temperature = models.DecimalField(null=True, decimal_places=2, max_digits=5, blank=True)
    nozzle = models.CharField(max_length=120, default='0.08')
    delay = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    rinsing_period = models.DecimalField(null=True, decimal_places=0, max_digits=6)


class StepSettings_Db(models.Model):
    x = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    y = models.DecimalField(null=True, decimal_places=2, max_digits=5)


class SampleApplication_Db(core_models.Application_Db):
    plate_size = models.OneToOneField(
        core_models.PlateSizeSettings_Db,
        on_delete=models.CASCADE,
    )

    offset = models.OneToOneField(
        core_models.OffsetSettings_Db,
        on_delete=models.CASCADE,
    )

    zero_position = models.OneToOneField(
        core_models.ZeroPosition_Db,
        on_delete=models.CASCADE,
    )

    band_settings = models.OneToOneField(
        BandSettings_Db,
        on_delete=models.CASCADE,
    )

    application_settings = models.OneToOneField(
        ApplicationSettings_Db,
        on_delete=models.CASCADE,
    )

    step_settings = models.OneToOneField(
        StepSettings_Db,
        on_delete=models.CASCADE,
    )


class BandsComponents_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                           related_name='band_components',
                                           null=True,
                                           on_delete=models.CASCADE,
                                           blank=True)
    band_number = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
    product_name = models.CharField(null=True, max_length=120, blank=True)
    company = models.CharField(null=True, max_length=120, blank=True)
    region = models.CharField(null=True, max_length=120, blank=True)
    year = models.DecimalField(decimal_places=0, max_digits=6, null=True, blank=True)
    volume = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    type = models.CharField(null=True, max_length=120, blank=True)
    density = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    viscosity = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
