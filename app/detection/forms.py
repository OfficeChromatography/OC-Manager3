from django import forms
from django.forms import ModelForm
from .models import CameraControls_Db, UserControls_Db
from django.contrib.auth.models import User

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

ROTATION = (('0','0'),
('1','90'),
('2','180'),
('3','270'))

EXPOSURE_METERING_MODES = ((0,'Averange'),(1,'Center Weighted'),(2,'Spot'))

SCENE_MODE = ((0,'None'),(8,'Night'),(11,'Sports'))

POWER_LINE_FREQUENCY = ((0,'Disable'),(1,'50 Hz'),(2,'60 Hz'),(3,'Auto'))

COLOR_EFFECT = {(0,'None'),
                (1,'Black & White'),
                (2,'Sepia'),
                (3,'Negative'),
                (4,'Emboss'),
                (5,'Sketch'),
                (6,'Sky Blue'),
                (7,'Grass Green'),
                (8,'Skin Whiten'),
                (9,'Vivid'),
                (10,'Aqua'),
                (11,'Art Freeze'),
                (12,'Silhouette'),
                (13,'Solarization'),
                (14,'Set Cb/Cr'),
                }


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

class CameraControlsForm(forms.ModelForm):
    # Camera Controls
        class Meta:
            model = CameraControls_Db

            fields =[   'auto_exposure',
                        'exposure_dynamic_framerate',
                        'auto_exposure_bias',
                        'exposure_time_absolute',
                        'exposure_metering_mode',
                        'white_balance_auto_preset',
                        'image_stabilization',
                        'iso_sensitivity_auto',
                        'iso_sensitivity',
                        'scene_mode']
            widgets = {
                        'auto_exposure':                forms.Select(attrs={'class': 'form-control'}),
                        'exposure_dynamic_framerate':   forms.NullBooleanSelect(attrs={'class': 'form-control'}),
                        'white_balance_auto_preset':    forms.Select(attrs={'class': 'form-control'}),
                        'image_stabilization':          forms.NullBooleanSelect(attrs={'class': 'form-control'}),
                        'iso_sensitivity':              forms.Select(attrs={'class': 'form-control'}),
                        'iso_sensitivity_auto':         forms.Select(attrs={'class': 'form-control'}),
                        'exposure_metering_mode':       forms.Select(attrs={'class': 'form-control'}),
                        'scene_mode':                   forms.Select(attrs={'class': 'form-control'}),
            }
            labels = {
                        'auto_exposure':                _('Auto Exposure:'),
                        'exposure_dynamic_framerate':   _('Exposure Dynamic FR:'),
                        'auto_exposure_bias':           _('Auto Exposure Bias'),
                        'white_balance_auto_preset':    _('WB Preset'),
                        'image_stabilization':          _('Image Stabilization'),
                        'iso_sensitivity':              _('ISO'),
                        'iso_sensitivity_auto':         _('ISO Auto'),
                        'exposure_metering_mode':       _('Exposure Metering Mode'),
                        'scene_mode':                   _('Scene Mode'),
            }


        auto_exposure_bias = forms.DecimalField(label='Auto Exposure Bias',
                                required=False,
                                max_digits=2,
                                decimal_places=0,
                                max_value=24,
                                min_value=0,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'12', 'class':'form-control'}))

        exposure_time_absolute = forms.DecimalField(label='Absolute Exposure Time',
                                required=False,
                                max_digits=5,
                                decimal_places=0,
                                max_value=10000,
                                min_value=1,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1000', 'class':'form-control'}))


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

class UserControlsForm(forms.ModelForm):
    class Meta:
        model = UserControls_Db
        fields = [
                     'brightness',
                       'contrast',
                     'saturation',
                    'red_balance',
                   'blue_balance',
                'horizontal_flip',
                  'vertical_flip',
           'power_line_frequency',
                      'sharpness',
                  'color_effects',
                         'rotate',
             'color_effects_cbcr',

        ]
        widgets = {
               'horizontal_flip':   forms.NullBooleanSelect(attrs={'class': 'form-control'}),
                 'vertical_flip':   forms.NullBooleanSelect(attrs={'class': 'form-control'}),
          'power_line_frequency':   forms.Select(attrs={'class': 'form-control'}),
                 'color_effects':   forms.Select(attrs={'class': 'form-control'}),
                    }
        labels = {
                'horizontal_flip':          _('Horizontal Flip:'),
                'vertical_flip':            _('Vertical Flip:'),
                'power_line_frequency':     _('Power Line Frequency:'),
                'color_effects':            _('Color Effect:'),
                }



    brightness = forms.DecimalField(label='Brightness',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1000', 'class':'form-control'}))

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

    rotate = forms.DecimalField(label='Rotate',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=360,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'step':'90' ,'class':'form-control'}))

    color_effects_cbcr = forms.DecimalField(label='Color Effect CbCr',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=65535,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'32896', 'class':'form-control'}))

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


class ShootConfigurationForm(forms.Form):

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


    pixelformat = forms.ChoiceField(label='Formats', choices = FORMATS, widget=forms.Select(attrs={'class':'form-control'}))



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



    def clean_pixelformat(self):
        pixelformat = self.cleaned_data['pixelformat']
        pixelformat = FORMATS[int(pixelformat)][1]
        return pixelformat
