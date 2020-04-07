from django import forms
from django.contrib.auth.models import User
# try:
#     from picamera import PiCamera
#     AWB_MODES = PiCamera.AWB_MODES
#     # EXPOSURE_MODES
#     # IMAGE_EFFECTS
# except OSError:
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
EXPOSURE_MODES = (('0', 'off'),
                ('1', 'auto'),
                ('2', 'night'),
                ('3', 'nightpreview'),
                ('4', 'backlight'),
                ('5', 'spotlight'),
                ('6', 'sports'),
                ('7', 'snow'),
                ('8', 'beach'),
                ('9', 'verylong'),
                ('10', 'fixedfps'),
                ('11', 'antishake'),
                ('12', 'fireworks'))
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

class ShootConfigurationForm(forms.Form):
    # # awb_mode = should be in off if we want to control using awb_gains los valores posibles se pueden sacar de PiCamera.AWB_MODES
    # awb_mode = forms.ChoiceField(label='AWB Modes', choices = AWB_MODES)
    # # # awb_gains = (red,blue)  -  0.0~8.0
    # awb_gains_red = forms.DecimalField(label='Red', max_digits=2, decimal_places=1, max_value=8, min_value=0)
    # awb_gains_blue = forms.DecimalField(label='Blue',max_digits=2, decimal_places=1, max_value=8, min_value=0)

    # brigthnes = 0~100 dafult 50
    brightness = forms.DecimalField(label='Brightness' ,max_digits=3, decimal_places=0, max_value=100, min_value=0, widget=forms.NumberInput(attrs={'size': '9', 'class':'form-control'}))
    # contrast = -100~100
    contrast = forms.DecimalField(label='Contrast',max_digits=3, decimal_places=0, max_value=100, min_value=-100, widget=forms.NumberInput(attrs={'size': '9', 'class':'form-control'}))

    # saturation = -100~100  default 0
    saturation = forms.DecimalField(label='Saturation', max_digits=3, decimal_places=0, max_value=100, min_value=-100, widget=forms.NumberInput(attrs={'size': '9', 'class':'form-control'}))
    # sharpeness = -100~100 default 0
    sharpeness = forms.DecimalField(label='Sharpeness', max_digits=3, decimal_places=0, max_value=100, min_value=-100, widget=forms.NumberInput(attrs={'size': '9', 'class':'form-control'}))

    # # color_effects = (u,v) - 0 ~ 255  default 128,128
    # color_effects_u = forms.DecimalField(label='u',max_digits=3, decimal_places=0, max_value=255, min_value=0)
    # color_effects_v = forms.DecimalField(label='v',max_digits=3, decimal_places=0, max_value=255, min_value=0)


    # # exposure_mode = '' los valores posibles se pueden sacar de PiCamera.EXPOSURE_MODES
    # exposure_mode = forms.ChoiceField(label='Exp Mode', choices = AWB_MODES)
    # # exposure_compensation = -25~25
    # exposure_compensation = forms.DecimalField(label='Exp Compensation',max_digits=2, decimal_places=0, max_value=25, min_value=-25)

    # # image_effect = PiCamera.IMAGE_EFFECTS
    # image_effect = forms.ChoiceField(label='Image Effect', choices = IMAGE_EFFECTS)
    # # image_effect_param
    #

    # resolution
    resolution = forms.CharField(
                    label='Resolution',
                    max_length = 9,
                    widget=forms.TextInput(
                                        attrs={
                                                'size': '9',
                                                'class':'form-control',
                                                'data-toggle':"tooltip",
                                                'data-placement':'top',
                                                'title':"E.g. 1024x1024",
                                                }
                                            )
                                        )
    framerate = forms.DecimalField(label='Framerate',
                    max_digits=3,
                    decimal_places=1,
                    max_value=15,
                    min_value=0.1,
                    widget=forms.NumberInput(
                                        attrs={
                                                'class':'form-control',
                                                'data-toggle':'tooltip',
                                                'data-placement':'top',
                                                'title':"E.g. 0.6 or 5",
                                                }
                                            )
                                        )
    # shutter_speed = 0 automatic / its in us / it is limited by the framrate, MUST set before a extrmely slow framrate \ 1/fps es lo mas lento
    shutter_speed = forms.DecimalField(
                        label='Shutter speed',
                        max_digits=6,
                        decimal_places=0,
                        max_value=30000,
                        min_value=0,
                        widget=forms.NumberInput(
                                        attrs={
                                                'class':'form-control',
                                                'data-toggle':'tooltip',
                                                'data-placement':'top',
                                                'data-html':"true",

                                                'title':"E.g. 33000<br>Less than 1/framerate",
                                                }
                                            )
                                        )
    # iso = 100~800
    iso = forms.ChoiceField(label='ISO', choices = ISO, widget=forms.Select(attrs={'class':'form-control'}))

    # # rotation = 0 90 180 270
    # rotation = forms.ChoiceField(label='Rotation', choices = ROTATION)
    # # vflip = True/False
    # vflip = forms.BooleanField(label='Vertical Flip')
    # # hflip = True False
    # hflip = forms.BooleanField(label='Horizontal Flip')
    # # zoom = tupple of float (x,y,w,h) default=(0,0,1.0,1.0)
    # zoom_x = forms.DecimalField(label='X',max_digits=2, decimal_places=1, max_value=1, min_value=0)
    # zoom_y = forms.DecimalField(label='Y',max_digits=2, decimal_places=1, max_value=1, min_value=0)
    # zoom_width = forms.DecimalField(label='Width',max_digits=2, decimal_places=1, max_value=1, min_value=0)
    # zoom_heigth = forms.DecimalField(label='Heigth',max_digits=2, decimal_places=1, max_value=1, min_value=0)
    def TakeaPhoto(self):
        try:
            camera = PiCamera()
            camera.resolution = self.cleaned_data.get('resolution')
            camera.framerate = self.cleaned_data.get('framerate')
            camera.iso = self.cleaned_data.get('iso')
            camera.shutter_speed = self.cleaned_data.get('shutter_speed')
            camera.capture('/ejemplo')
        except:
            print('PiCamera not connected')
