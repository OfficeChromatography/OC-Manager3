from django.forms import ModelForm
from django import forms
from .models import PlateProperties_Db, SampleApplication_Db, BandSettings_Db, MovementSettings_Db, PressureSettings_Db, BandsComponents_Db
PROP_CHOICES =(
    ("1", "N Bands"),
    ("2", "Lenght"),
)

class SampleApplication_Form(forms.ModelForm):
    class Meta:
        model = SampleApplication_Db
        fields = ['file_name']
        widgets = {
            'file_name':        forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'file_name':        _('Filename'),
        }
        error_messages = {
            'file_name': {
                'max_length': _("This name is too long."),
            },
        }

class PlateProperties_Form(forms.ModelForm):
    class Meta:
        model = PlateProperties_Db
        fields = ['size_x','size_y','offset_left','offset_right','offset_top','offset_bottom']
        widgets = {
            'size_y' : forms.NumberInput(attrs={'class': 'form-control'}),
            'size_x' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_left' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_right' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_top' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_bottom' : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'size_y':           _('Y Size'),
            'size_x':           _('X Size'),
            'offset_left':      _('Left'),
            'offset_right':     _('Right'),
            'offset_top':       _('Top'),
            'offset_bottom':    _('Bottom'),
        }

class BandSettings_Form(forms.ModelForm):
    class Meta:
        model = BandSettings_Db
        fields = ['main_property','value','height','gap']
        widgets = {
            'main_property' : forms.Select(choices=PROP_CHOICES, attrs={'class': 'form-control'}),
            'value'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'height'    : forms.NumberInput(attrs={'class': 'form-control'}),
            'gap'       : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'main_property' : _('Main Property'),
            'value'         : _('Value'),
            'height'        : _('Height'),
            'gap'           : _('Gap'),
        }

class MovementSettings_Form(forms.ModelForm):
    class Meta:
        model = MovementSettings_Db
        fields = ['motor_speed','delta_x','delta_y']
        widgets = {
            'motor_speed'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'delta_x'       : forms.NumberInput(attrs={'class': 'form-control'}),
            'delta_y'       : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'motor_speed' : _('MotorSpeed'),
            'delta_x'     : _('Delta X'),
            'delta_y'     : _('Delta Y'),
        }

class PressureSettings_Form(forms.ModelForm):
    class Meta:
        model = PressureSettings_Db
        fields = ['pressure','frequency', 'temperature']
        widgets = {
            'pressure'              : forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency'             : forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature'           : forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BandsComponents_Form(forms.ModelForm):
    class Meta:
        model = BandsComponents_Db
        fields = ['band_number','description', 'volume', 'type']
        exclude = ['sample_application']

    def clean_band_number(self):
        band_number = self.cleaned_data.get("band_number")
        return band_number

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description

    def clean_volume(self):
        volume = self.cleaned_data.get('volume')
        return volume

    def clean_type(self):
        type = self.cleaned_data.get('type')
        return type
