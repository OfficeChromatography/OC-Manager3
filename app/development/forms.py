from django.forms import ModelForm
from django import forms
from .models import *


class Development_Form(forms.ModelForm):
    class Meta:
        model = Development_Db
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
        initial['offset_bottom'] = 2
        kwargs['initial'] = initial
        super(PlateProperties_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = PlateProperties_Dev_Db
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

class DevelopmentBandSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['volume'] = 1000
        initial['applications'] = 10
        initial['precision'] = 10
        initial['fluid'] = 'Methanol'
        initial['waitTime'] = 0
        kwargs['initial'] = initial
        super(DevelopmentBandSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = BandSettings_Dev_Db
        fields = ['volume','fluid','applications','precision','waitTime','printBothways','density','viscosity']
        widgets = {
            'volume'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'fluid'    : forms.Select(attrs={'class': 'form-control'}, choices=[
                ('n-Hexane','n-Hexane'),
                ('Pentane','Pentane'),
                ('Cyclohexane','Cyclohexane'),
                ('Carbon Tetrachloride','Carbon Tetrachloride'),
                ('Toluene','Toluene'),
                ('Chloroform','Chloroform'),
                ('Dichloromethane','Dichloromethane'),
                ('Diethyl ether','Diethyl ether'),
                ('Ethyl acetate','Ethyl acetate'),
                ('Acetone','Acetone'),
                ('Ethanol','Ethanol'),
                ('Methanol','Methanol'),
                ('Pyridine','Pyridine'),
                ('Water','Water'),
                ('Specific','Specific')
            ]),
            'applications'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'precision'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'waitTime'   : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'volume'         : _('Volume'),
            'fluid'         : _('Fluid'),
            'applications'   : _('Applications'),
            'precision'   : _('Pressure Checks'),
            'waitTime'    : _('Waiting Time'),
        }

        def clean(self):
            fluid = self.cleaned_data.get("fluid")
            density = self.cleaned_data.get("density")
            viscosity = self.cleaned_data.get("viscosity")
            if fluid == 'Specific':
                if density == "null" or viscosity == "null":
                    raise forms.ValidationError(
                        "Specify Density and Viscosity!"
                    )
            return self.cleaned_data
            
class PressureSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['pressure'] = 10
        initial['temperature'] = 0
        kwargs['initial'] = initial
        super(PressureSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = PressureSettings_Dev_Db
        fields = ['temperature','nozzlediameter','pressure']
        widgets = {
            'temperature'           : forms.NumberInput(attrs={'class': 'form-control'}),
            'nozzlediameter'        : forms.Select(attrs={'class': 'form-control'}, choices=[
                ('0.25','0.25'),
                ('0.19','0.19'),
                ('0.13','0.13'),
                ('0.10','0.10'),
                ('0.08','0.08'),
                ('0.05','0.05'),
            ]),
            'pressure'           : forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'pressure'         : _('Pressure')
        }

        def clean_temperature(self):
            temperature = self.temperature
            if not temperature:
                return 0
