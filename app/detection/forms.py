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

AUTO_EXPOSURE = (('0', 'off'),
                ('1', 'auto'))

ISO_SENSITIVITY =   ((0,0),
                    (1,100000),
                    (2,200000),
                    (3,400000),
                    (4,900000))

ISO_SENSITIVITY_AUTO =  ((0,'Manual'),
                        (1,'Auto'))
FORMATS = ((0,'YU12'),    # (Planar YUV 4:2:0)
            (1,'YUYV'),    # (YUYV 4:2:2)
            (2,'RGB3'),    # (24-bit RGB 8-8-8)
            (3,'JPEG'),    # (JFIF JPEG, compressed)
            (4,'H264'),    # (H.264, compressed)
            (5,'MJPG'),    # (Motion-JPEG, compressed)
            (6,'YVYU'),    # (YVYU 4:2:2)
            (7,'VYUY'),    # (VYUY 4:2:2)
            (8,'UYVY'),    # (UYVY 4:2:2)
            (9,'NV12'),    # (Y/CbCr 4:2:0)
            (10,'BGR3'),   # (24-bit BGR 8-8-8)
            (11,'YV12'),   # (Planar YVU 4:2:0)
            (12,'NV21'),   # (Y/CrCb 4:2:0)
            (13,'BGR4'))   # (32-bit BGRA/X 8-8-8-8))


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

class SaveShot(forms.Form):
    name = forms.CharField(label='Name',
                    required=True,
                    max_length = 9,
                    widget=forms.TextInput(
                                        attrs={
                                                'size': '9',
                                                'placeholder':'FileName',
                                                'class':'form-control',
                                                'data-toggle':"tooltip",
                                                'data-placement':'top',
                                                'title':"Please insert a name to save your Photo",
                                                }
                                            )
                                        )

class ShootConfigurationForm(forms.Form):
    # User Controls
    #
                   #   brightness 0x00980900 (int)    : min=0 max=100 step=1 default=50 value=50 flags=slider
                   #     contrast 0x00980901 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
                   #   saturation 0x00980902 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
                   #  red_balance 0x0098090e (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
                   # blue_balance 0x0098090f (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
                   # sharpness 0x0098091b (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider

    #             horizontal_flip 0x00980914 (bool)   : default=0 value=0
    #               vertical_flip 0x00980915 (bool)   : default=0 value=0
    #        power_line_frequency 0x00980918 (menu)   : min=0 max=3 default=1 value=1

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

    sharpness = forms.DecimalField(label='Sharpness',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=-100,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))

# Camera Controls
#
            #                   auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=0 value=0
            #          exposure_time_absolute 0x009a0902 (int)    : min=1 max=10000 step=1 default=1000 value=1000
#      exposure_dynamic_framerate 0x009a0903 (bool)   : default=0 value=0
#              auto_exposure_bias 0x009a0913 (intmenu): min=0 max=24 default=12 value=12
#       white_balance_auto_preset 0x009a0914 (menu)   : min=0 max=10 default=1 value=1
#             image_stabilization 0x009a0916 (bool)   : default=0 value=0
    #                 iso_sensitivity 0x009a0917 (intmenu): min=0 max=4 default=0 value=0
    #            iso_sensitivity_auto 0x009a0918 (menu)   : min=0 max=1 default=1 value=1
#          exposure_metering_mode 0x009a0919 (menu)   : min=0 max=2 default=0 value=0
#                      scene_mode 0x009a091a (menu)   : min=0 max=13 default=0 value=0



# Camera Controls

    auto_exposure = forms.ChoiceField(label='Auto Exposure', choices = AUTO_EXPOSURE, widget=forms.Select(attrs={'class':'form-control'}))

    exposure_time_absolute = forms.DecimalField(label='Absolute Exposure Time',
                            required=False,
                            max_digits=5,
                            decimal_places=0,
                            max_value=10000,
                            min_value=1,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'50', 'class':'form-control'}))

    iso_sensitivity = forms.ChoiceField(label='ISO Sensitivity', choices = ISO_SENSITIVITY, widget=forms.Select(attrs={'class':'form-control'}))

    iso_sensitivity_auto = forms.ChoiceField(label='ISO Sensitivity auto', choices = ISO_SENSITIVITY_AUTO, widget=forms.Select(attrs={'class':'form-control'}))

# Frame_Controls

    resolution = forms.CharField(label='Resolution',
                    required=False,
                    max_length = 9,
                    widget=forms.TextInput(
                                        attrs={
                                                'size': '9',
                                                'placeholder':'WIDTHxHEIGHT',
                                                'class':'form-control',
                                                'data-toggle':"tooltip",
                                                'data-placement':'top',
                                                'title':"def. 1024x1024",
                                                }
                                            )
                                        )

    framerate = forms.DecimalField(label='Framerate',
                    max_digits=3,
                    required=False,
                    decimal_places=1,
                    max_value=90,
                    min_value=1,
                    widget=forms.NumberInput(
                                        attrs={
                                                'class':'form-control',
                                                'data-toggle':'tooltip',
                                                'data-placement':'top',
                                                'placeholder':'1.0',
                                                }
                                            )
                                        )

    pixelformat = forms.ChoiceField(label='Formats', choices = FORMATS, widget=forms.Select(attrs={'class':'form-control'}))









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
            saturation = 0
        return saturation

    def clean_red_balance(self):
        red_balance = self.cleaned_data['red_balance']
        if red_balance:
            red_balance = int(red_balance)
        if not red_balance:
            red_balance = 1000
        return red_balance

    def clean_blue_balance(self):
        blue_balance = self.cleaned_data['blue_balance']
        if blue_balance:
            blue_balance = int(blue_balance)
        if not blue_balance:
            blue_balance = 1000
        return blue_balance

    def clean_sharpness(self):
        sharpness = self.cleaned_data['sharpness']
        if sharpness:
            sharpness = int(sharpness)
        if not sharpness:
            sharpness = 0
        return sharpness

    def clean_auto_exposure(self):
        auto_exposure = self.cleaned_data['auto_exposure']
        if auto_exposure:
            auto_exposure = int(auto_exposure)
        if not auto_exposure:
            auto_exposure = 0
        return auto_exposure

    def clean_exposure_time_absolute(self):
        exposure_time_absolute = self.cleaned_data['exposure_time_absolute']
        if exposure_time_absolute:
            exposure_time_absolute = int(exposure_time_absolute)
        if not exposure_time_absolute:
            exposure_time_absolute = 1000
        return exposure_time_absolute

    def clean_iso_sensitivity(self):
        iso_sensitivity = self.cleaned_data['iso_sensitivity']
        if iso_sensitivity:
            iso_sensitivity = int(iso_sensitivity)
        if not iso_sensitivity:
            iso_sensitivity = 0
        return iso_sensitivity

    def clean_iso_sensitivity_auto(self):
        iso_sensitivity_auto = self.cleaned_data['iso_sensitivity_auto']
        if iso_sensitivity_auto:
            iso_sensitivity_auto = int(iso_sensitivity_auto)
        if not iso_sensitivity_auto:
            iso_sensitivity_auto = 0
        return iso_sensitivity_auto

    def clean_resolution(self):
        resolution = self.cleaned_data['resolution']
        if resolution:
            resolution = resolution.casefold()
            if not 'x':
                raise forms.ValidationError("Invalid Format.")
            else:
                position = resolution.find('x')
                width = int(resolution[:position])
                height = int(resolution[position+1:])
        else:
            width = 640
            height = 480
        return [width, height]

    def clean_framerate(self):
        framerate = self.cleaned_data['framerate']
        if framerate:
            framerate = float(framerate)
        if not framerate:
            framerate = 1.0
        return framerate

    def clean_pixelformat(self):
        pixelformat = self.cleaned_data['pixelformat']
        pixelformat = FORMATS[int(pixelformat)][1]
        return pixelformat


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
