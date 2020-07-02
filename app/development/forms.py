from django.forms import ModelForm
from django import forms
from .models import Development_Db, PlateProperties_Dev_Db, BandSettings_Dev_Db, MovementSettings_Dev_Db, PressureSettings_Dev_Db


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
    class Meta:
        model = BandSettings_Dev_Db
        fields = ['volume','printBothways']
        widgets = {
            'volume'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'printBothways'   : forms.CheckboxInput(attrs={'class': 'form-control checkbox'}),
        }
        labels = {
            'volume'         : _('Volume'),
            'printBothways'         : _('print bothways'),
        }

class MovementSettings_Form(forms.ModelForm):
    class Meta:
        model = MovementSettings_Dev_Db
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
    class Meta:
        model = PressureSettings_Dev_Db
        fields = ['pressure','frequency', 'temperature']
        widgets = {
            'pressure'              : forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency'             : forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature'           : forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def clean_temperature(self):
            temperature = self.temperature
            if not temperature:
                return 0
