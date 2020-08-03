from django.db import models
from django.contrib.auth import get_user_model

AWB_MODES = (('0', 'off'),
            ('1', 'auto'),
            ('2', 'sunlight'),
            ('3', 'cloudy'),
            ('4', 'shade'),
            ('5', 'tungsten'),
            ('6', 'fluorescent'),
            ('7', 'incandescent'),
            ('8', 'flash'),
            ('9', 'horizon'))

AUTO_EXPOSURE = (('0', 'off'),
                ('1', 'auto'))

ISO_SENSITIVITY =   (('0',0),
                    ('1',100000),
                    ('2',200000),
                    ('3',400000),
                    ('4',900000))

ISO_SENSITIVITY_AUTO =  (('0','Manual'),
                        ('1','Auto'))
FORMATS = (('0','YU12'),    # (Planar YUV 4:2:0)
            ('1','YUYV'),    # (YUYV 4:2:2)
            ('2','RGB3'),    # (24-bit RGB 8-8-8)
            ('3','JPEG'),    # (JFIF JPEG, compressed)
            ('4','H264'),    # (H.264, compressed)
            ('5','MJPG'),    # (Motion-JPEG, compressed)
            ('6','YVYU'),    # (YVYU 4:2:2)
            ('7','VYUY'),    # (VYUY 4:2:2)
            ('8','UYVY'),    # (UYVY 4:2:2)
            ('9','NV12'),    # (Y/CbCr 4:2:0)
            ('10','BGR3'),   # (24-bit BGR 8-8-8)
            ('11','YV12'),   # (Planar YVU 4:2:0)
            ('12','NV21'),   # (Y/CrCb 4:2:0)
            ('13','BGR4'))   # (32-bit BGRA/X 8-8-8-8))


IMAGE_EFFECTS = (('0', 'none'),
                ('1', 'negative'),
                ('2', 'solarize'),
                ('6', 'sketch'),
                ('7', 'denoise'),
                ('8', 'emboss'),
                ('9', 'oilpaint'),
                ('10', 'hatch'),
                ('11', 'gpen'),
                ('12', 'pastel'),
                ('13', 'watercolor'),
                ('14', 'film'),
                ('15', 'blur'),
                ('16', 'saturation'),
                ('17', 'colorswap'),
                ('18', 'washedout'),
                ('19', 'posterise'),
                ('20', 'colorpoint'),
                ('21', 'colorbalance'),
                ('22', 'cartoon'),
                ('23', 'deinterlace1'),
                ('24', 'deinterlace2'))

ISO = (('0','Auto'),
('1','100'),
('2','200'),
('3','320'),
('4','400'),
('5','500'),
('6','640'),
('7','800'))

ROTATION = (('0','0'),
('1','90'),
('2','180'),
('3','270'))

EXPOSURE_METERING_MODES = (('0','Averange'),('1','Center Weighted'),('2','Spot'))

SCENE_MODE = (('0','None'),('8','Night'),('11','Sports'))

POWER_LINE_FREQUENCY = (('0','Disable'),('1','50 Hz'),('2','60 Hz'),('3','Auto'))

COLOR_EFFECT = (('0','None'),
                ('1','Black & White'),
                ('2','Sepia'),
                ('3','Negative'),
                ('4','Emboss'),
                ('5','Sketch'),
                ('6','Sky Blue'),
                ('7','Grass Green'),
                ('8','Skin Whiten'),
                ('9','Vivid'),
                ('10','Aqua'),
                ('11','Art Freeze'),
                ('12','Silhouette'),
                ('13','Solarization'),
                ('14','Set Cb/Cr'))
# class PhotoShootPropertiesModel(model.Model):
#     name = models.CharField(max_length=180)
#     description = models.TextField()


    # analog_gain =
        # analog_gain = Forms.DecimalField()
    # # awb_gains = (red,blue)  -  0.0~8.0
        # analog_gain_red = Forms.DecimalField(max_digits=2, decimal_places=1)
        # analog_gain_blue = Forms.DecimalField()
    # awb_mode = should be in off if we want to control using awb_gains los valores posibles se pueden sacar de PiCamera.AWB_MODES
    # brigthnes = 0~100 dafult 50
    # color_effects = (u,v) - 0 ~ 255  default 128,128
    # contrast = -100~100
    # digital_gain = solo es getter
    # exposure_compensation = -25~25
    # exposure_mode = '' los valores posibles se pueden sacar de PiCamera.EXPOSURE_MODES
    # exposure_speed
    # hflip = True False
    # image_effect = PiCamera.IMAGE_EFFECTS
    # image_effect_param
    # iso = 100~800
    # resolution
    # rotation = 0 90 180 270
    # saturation = -100~100  default 0
    # sharpeness = -100~100 default 0
    # shutter_speed = 0 automatic
    # vflip = True/False
    # zoom = tupple of float (x,y,w,h) default=(0,0,1.0,1.0)

class PlatePhoto_Db(models.Model):
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to='media/')

class CameraControls_Db(models.Model):
    auto_exposure = models.CharField(max_length=255, choices=AUTO_EXPOSURE, null=True, blank=True)

    exposure_dynamic_framerate = models.BooleanField(null=True, blank=True)

    auto_exposure_bias = models.DecimalField(
                            null=True,
                            blank=True,
                            max_digits=2,
                            decimal_places=0)

    exposure_time_absolute = models.DecimalField(
                            null=True,
                            blank=True,
                            max_digits=5,
                            decimal_places=0)

    white_balance_auto_preset = models.CharField(max_length=255, choices=AWB_MODES, null=True, blank=True)

    image_stabilization = models.BooleanField(null=True, blank=True)

    iso_sensitivity = models.CharField(max_length=255, choices = ISO_SENSITIVITY, null=True, blank=True)

    iso_sensitivity_auto = models.CharField(max_length=255, choices = ISO_SENSITIVITY_AUTO, null=True, blank=True)

    exposure_metering_mode = models.CharField(max_length=255, choices = EXPOSURE_METERING_MODES, null=True, blank=True)

    scene_mode = models.CharField(max_length=255, choices = SCENE_MODE, null=True, blank=True)

class UserControls_Db(models.Model):

    #
        #                      brightness (int)    : min=0 max=100 step=1 default=50 value=50 flags=slider
        #                        contrast (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
        #                      saturation (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
        #                     red_balance (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
        #                    blue_balance (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
    #                 horizontal_flip (bool)   : default=0 value=0
    #                   vertical_flip (bool)   : default=0 value=0
    #            power_line_frequency (menu)   : min=0 max=3 default=1 value=1
        #                       sharpness (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
    #                   color_effects (menu)   : min=0 max=15 default=0 value=0
    #                          rotate (int)    : min=0 max=360 step=90 default=0 value=0 flags=00000400
    #              color_effects_cbcr (int)    : min=0 max=65535 step=1 default=32896 value=32896

    brightness =    models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    contrast =     models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    saturation =     models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    red_balance =     models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=4,
                        decimal_places=0)

    blue_balance =     models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=4,
                        decimal_places=0)

    horizontal_flip =   models.BooleanField(null=True, blank=True)

    vertical_flip   =   models.BooleanField(null=True, blank=True)

    power_line_frequency = models.CharField(max_length=255, choices = POWER_LINE_FREQUENCY, null=True, blank=True)

    sharpness = models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    color_effects = models.CharField(max_length=255, choices = COLOR_EFFECT, null=True, blank=True)

    rotate = models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    color_effects_cbcr = models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=5,
                        decimal_places=0)

class Images_Db(models.Model):
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    url = models.CharField(max_length=100, null=True)
    path = models.CharField(max_length=200, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

class Leds_Db(models.Model):
    uv365_power = models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)

    uv278_power = models.DecimalField(
                        null=True,
                        blank=True,
                        max_digits=3,
                        decimal_places=0)
