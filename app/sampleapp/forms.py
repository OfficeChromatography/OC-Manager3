from django.forms import ModelForm
from django import forms
from .models import *


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
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['size_y'] = 100
        initial['size_x'] = 100
        initial['offset_left'] = 1
        initial['offset_right'] = 1
        initial['offset_top'] = 1
        initial['offset_bottom'] = 1
        kwargs['initial'] = initial
        super(PlateProperties_Form, self).__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['value'] = 2
        initial['height'] = 1
        initial['gap'] = 4
        kwargs['initial'] = initial
        super(BandSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = BandSettings_Db
        fields = ['main_property','value','height','gap']
        PROP_CHOICES =(
            ("1", "Number of Bands"),
            ("2", "Length"),
            )
        widgets = {
            'main_property' : forms.Select(choices=PROP_CHOICES, attrs={'class': 'form-control'}),
            'value'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'height'    : forms.NumberInput(attrs={'class': 'form-control'}),
            'gap'       : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'main_property' : _('Band Calculation'),
            'value'         : _('Number'),
            'height'        : _('Height'),
            'gap'           : _('Gap'),
        }

        def clean_main_property(self):
            return int(self.main_property)

class MovementSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['motor_speed'] = 1000
        initial['delta_x'] = 1
        initial['delta_y'] = 1
        kwargs['initial'] = initial
        super(MovementSettings_Form, self).__init__(*args, **kwargs)
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

        def clean_motor_speed(self):
            motor_speed = self.motor_speed
            return int(motor_speed)


class PressureSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['pressure'] = 25
        initial['frequency'] = 1400
        initial['temperature'] = 0
        kwargs['initial'] = initial
        super(PressureSettings_Form, self).__init__(*args, **kwargs)
    class Meta:
        model = PressureSettings_Db
        fields = ['pressure','frequency', 'temperature','nozzlediameter']
        widgets = {
            'pressure'              : forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency'             : forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature'           : forms.NumberInput(attrs={'class': 'form-control'}),
            'nozzlediameter'        : forms.Select(attrs={'class': 'form-control'}, choices=[
                ('0.25','0.25'),
                ('0.19','0.19'),
                ('0.13','0.13'),
                ('0.10','0.10'),
                ('0.08','0.08'),
                ('0.05','0.05'),
            ]),
        }
        def clean_temperature(self):
            temperature = self.temperature
            if not temperature:
                return 0

class BandsComponents_Form(forms.ModelForm):
    class Meta:
        model = BandsComponents_Db
        fields = ['band_number','description', 'volume', 'type', 'density', 'viscosity']
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
    
    def clean_density(self):
        density = self.cleaned_data.get('density')
        return density

    def clean_viscosity(self):
        viscosity = self.cleaned_data.get('viscosity')
        return viscosity

    def clean(self):
        viscosity = self.cleaned_data.get('viscosity')
        density = self.cleaned_data.get('density')
        type = self.cleaned_data.get('type')

        if type == 'Specific':
            if density == "null" or viscosity == "null":
                    raise forms.ValidationError(
                        "Specify Density and Viscosity!"
                    )
        return self.cleaned_data


