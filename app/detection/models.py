from django.db import models

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
