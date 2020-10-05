from django.forms import ModelForm
from .models import CleaningProcess_Db, ZeroPosition
from django import forms

class CleaningProcessForm(forms.ModelForm):
    class Meta:
        model = CleaningProcess_Db
        fields = [  'start_frequency',
                    'stop_frequency',
                    'steps',
                    'pressure',]

        widgets = {
                    'start_frequency':  forms.NumberInput(attrs={'class': 'form-control'}),
                    'stop_frequency':   forms.NumberInput(attrs={'class': 'form-control'}),
                    'steps':            forms.NumberInput(attrs={'class': 'form-control', 'max':'5'}),
                    'pressure':         forms.NumberInput(attrs={'class': 'form-control'}),
                    }
        labels = {

                    'start_frequency':          _('Start Frequency:'),
                    'stop_frequency':           _('Stop Frequency:'),
                    'steps':                    _('Steps:'),
                    'pressure':                 _('Horizontal Flip:'),
                }

    start_frequency = forms.DecimalField(label='Start Frequency',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=500,
                            min_value=100,
                            widget=forms.NumberInput(attrs={'size': '1', 'placeholder':'100', 'class':'form-control'}))

    stop_frequency = forms.DecimalField(label='Stop Frequency',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=500,
                            min_value=100,
                            widget=forms.NumberInput(attrs={'size': '1', 'placeholder':'500', 'class':'form-control'}))

    steps = forms.DecimalField(label='Steps',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=100,
                            min_value=50,
                            widget=forms.NumberInput(attrs={'size': '1', 'placeholder':'50', 'class':'form-control'}))

    pressure = forms.DecimalField(label='Pressure',
                            required=False,
                            max_digits=3,
                            decimal_places=0,
                            max_value=20,
                            min_value=14,
                            widget=forms.NumberInput(attrs={'size': '1', 'placeholder':'200', 'class':'form-control'}))

    def clean_start_frequency(self):
        return int(self.cleaned_data['start_frequency'])
    def clean_stop_frequency(self):
        return int(self.cleaned_data['stop_frequency'])
    def clean_steps(self):
        return int(self.cleaned_data['steps'])
    def clean_pressure(self):
        return int(self.cleaned_data['pressure'])

class ZeroPosition_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['zero_x'] = 4
        initial['zero_y'] = 19
        kwargs['initial'] = initial
        super(ZeroPosition_Form, self).__init__(*args, **kwargs)
    class Meta:
        model = ZeroPosition
        fields = ['zero_x','zero_y']
        widgets = {
            'zero_x'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'zero_y'   : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'zero_x'     : _('X0'),
            'zero_y'     : _('Y0'),
        }


