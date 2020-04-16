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
    # User Controls
    #
                   #   brightness 0x00980900 (int)    : min=0 max=100 step=1 default=50 value=50 flags=slider
                   #     contrast 0x00980901 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
                   #   saturation 0x00980902 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
                   #  red_balance 0x0098090e (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
                   # blue_balance 0x0098090f (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider

    #             horizontal_flip 0x00980914 (bool)   : default=0 value=0
    #               vertical_flip 0x00980915 (bool)   : default=0 value=0
    #        power_line_frequency 0x00980918 (menu)   : min=0 max=3 default=1 value=1
    #                   sharpness 0x0098091b (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
    #               color_effects 0x0098091f (menu)   : min=0 max=15 default=0 value=0
    #                      rotate 0x00980922 (int)    : min=0 max=360 step=90 default=0 value=0 flags=modify-layout
    #          color_effects_cbcr 0x0098092a (int)    : min=0 max=65535 step=1 default=32896 value=32896


# USER CONTROLS:

    brightness = forms.DecimalField(label='Brightness',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'50', 'class':'form-control'}))

    contrast = forms.DecimalField(label='Contrast',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=-100,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))

    # saturation = -100~100  default 0
    saturation = forms.DecimalField(label='Saturation',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=-100,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))

    red_balance =  forms.DecimalField(label='Red balance',
                            required=False,
                            max_digits=4,
                            decimal_places=0,
                            max_value=7999,
                            min_value=1,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1000', 'class':'form-control'}))

    blue_balance =  forms.DecimalField(label='Blue balance',
                            required=False,
                            max_digits=4,
                            decimal_places=0,
                            max_value=7999,
                            min_value=1,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1000', 'class':'form-control'}))

    # hue = forms.DecimalField(label='HUE',
    #                         required=False,
    #                         max_digits=4,
    #                         decimal_places=0,
    #                         max_value=2000,
    #                         min_value=-2000,
    #                         widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'50', 'class':'form-control'}))
    #
    # gain = forms.DecimalField(label='Gain',
    #                         required=False,
    #                         max_digits=1,
    #                         decimal_places=0,
    #                         max_value=8,
    #                         min_value=1,
    #                         widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'50', 'class':'form-control'}))
    #
    # exposure = forms.DecimalField(label='Exposure',
    #                         required=False,
    #                         max_digits=4,
    #                         decimal_places=0,
    #                         max_value=1000,
    #                         min_value=-1000,
    #                         widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'50', 'class':'form-control'}))


    # def clean_resolution(self):
    #     resolution = self.cleaned_data['resolution']
    #     if resolution:
    #         resolution = resolution.casefold()
    #         if not 'x':
    #             raise forms.ValidationError("Invalid Format.")
    #         else:
    #             position = resolution.find('x')
    #             width = int(resolution[:position])
    #             height = int(resolution[position+1:])
    #     else:
    #         width = 640
    #         height = 480
    #     return [width, height]
    #
    # def clean_framerate(self):
    #     framerate = self.cleaned_data['framerate']
    #     if framerate:
    #         framerate = float(framerate)
    #     if not framerate:
    #         framerate = 1.0
    #     return framerate
    #
    # def clean_shutter_speed(self):
    #     shutter_speed = self.cleaned_data['shutter_speed']
    #     if not shutter_speed:
    #         shutter_speed = 1.0
    #     else:
    #         framerate = self.clean_framerate()
    #         if shutter_speed > (1000000/framerate):
    #             raise forms.ValidationError("Invalid Format. Should be less than 1/framerate")
    #     return float(shutter_speed)

    def clean_brightness(self):
        brightness = self.cleaned_data['brightness']
        if brightness:
            brightness = int(brightness)
        if not brightness:
            brightness = 50
        return brightness

    def clean_contrast(self):
        contrast = self.cleaned_data['contrast']
        if contrast:
            contrast = int(contrast)
        if not contrast:
            contrast = 0
        return contrast

    def clean_saturation(self):
        saturation = self.cleaned_data['saturation']
        if saturation:
            saturation = int(saturation)
        if not saturation:
            saturation = 50
        return saturation

    def clean_red_balance(self):
        red_balance = self.cleaned_data['red_balance']
        if red_balance:
            red_balance = int(red_balance)
        if not red_balance:
            red_balance = 1000
        return red_balance

    def clean_blue_balance(self):
        blue_balance = self.cleaned_data['red_balance']
        if blue_balance:
            blue_balance = int(blue_balance)
        if not blue_balance:
            blue_balance = 1000
        return blue_balance
    # def clean_hue(self):
    #     hue = self.cleaned_data['hue']
    #     if hue:
    #         hue = int(hue)
    #     if not hue:
    #         hue = 50
    #     return hue
    #
    # def clean_gain(self):
    #     gain = self.cleaned_data['gain']
    #     if gain:
    #         gain = int(gain)
    #     if not gain:
    #         gain = 50
    #     return gain
    #
    # def clean_exposure(self):
    #     exposure = self.cleaned_data['exposure']
    #     if exposure:
    #         exposure = int(exposure)
    #     if not exposure:
    #         exposure = 50
    #     return exposure










            # resolution

            # resolution = forms.CharField(
            #                 label='Resolution',
            #                 required=False,
            #                 max_length = 9,
            #                 widget=forms.TextInput(
            #                                     attrs={
            #                                             'size': '9',
            #                                             'placeholder':'WIDTHxHEIGHT',
            #                                             'class':'form-control',
            #                                             'data-toggle':"tooltip",
            #                                             'data-placement':'top',
            #                                             'title':"def. 1024x1024",
            #                                             }
            #                                         )
            #                                     )
            # framerate = forms.DecimalField(label='Framerate',
            #                 max_digits=3,
            #                 required=False,
            #                 decimal_places=1,
            #                 max_value=15,
            #                 min_value=0.1,
            #                 widget=forms.NumberInput(
            #                                     attrs={
            #                                             'class':'form-control',
            #                                             'data-toggle':'tooltip',
            #                                             'data-placement':'top',
            #                                             'placeholder':'1.0',
            #                                             'title':"E.g. 0.6 or 5",
            #                                             }
            #                                         )
            #                                     )
            # shutter_speed = 0 automatic / its in us / it is limited by the framrate, MUST set before a extrmely slow framrate \ 1/fps es lo mas lento
            # shutter_speed = forms.DecimalField(
            #                     label='Shutter speed',
            #                     required=False,
            #                     max_digits=6,
            #                     decimal_places=0,
            #                     max_value=30000,
            #                     min_value=0,
            #                     widget=forms.NumberInput(
            #                                     attrs={
            #                                             'class':'form-control',
            #                                             'data-toggle':'tooltip',
            #                                             'data-placement':'top',
            #                                             'data-html':"true",
            #                                             'placeholder':'1.0',
            #                                             'title':"E.g. 33000<br>Less than 1/framerate",
            #                                             }
            #                                         )
            #                                     )
            # iso = 100~800
            #iso = forms.ChoiceField(label='ISO', choices = ISO, widget=forms.Select(attrs={'class':'form-control'}))
