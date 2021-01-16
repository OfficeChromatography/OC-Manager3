from django.forms import ModelForm
from django import forms
from .models import *


class Development_Form(forms.ModelForm):
    class Meta:
        model = Development_Db
        fields = ['filename']

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

    # printBothways = forms.BooleanField()

    class Meta:
        model = BandSettings_Dev_Db
        fields = ['volume', 'fluid', 'applications', 'printBothways','waitTime', 'density', 'viscosity', 'description']

    def clean(self):
        if self.cleaned_data.get('printBothways'):
            self.cleaned_data['printBothways']="True"
        else:
            self.cleaned_data['printBothways']="False"
        return self.cleaned_data

class PressureSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['pressure'] = 10
        initial['speed'] = 25
        initial['temperature'] = 0
        kwargs['initial'] = initial
        super(PressureSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = PressureSettings_Dev_Db
        fields = ['temperature','nozzlediameter','pressure','speed']
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
            'speed'           : forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'pressure'         : _('Pressure'),
            'speed'         : _('Speed')
        }

        def clean_temperature(self):
            temperature = self.temperature
            if not temperature:
                return 0

class Flowrate_Form(forms.ModelForm):
    class Meta:
        model = Flowrate_Db
        fields = ['value']
