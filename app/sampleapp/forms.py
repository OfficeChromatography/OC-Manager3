from django.forms import ModelForm
from django import forms
from .models import PlateProperties_Db, SampleApplication_Db, BandSettings_Db, MovementSettings_Db, PressureSettings_Db
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
                'max_length': _("This writer's name is too long."),
            },
        }

class PlateProperties_Form(forms.ModelForm):
    class Meta:
        model = PlateProperties_Db
        fields = ['size_x','size_y','offset_x','offset_y']
        widgets = {
            'size_y' : forms.NumberInput(attrs={'class': 'form-control'}),
            'size_x' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_x' : forms.NumberInput(attrs={'class': 'form-control'}),
            'offset_y' : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'size_y':       _('Y Size'),
            'size_x':       _('X Size'),
            'offset_x':     _('X Offset'),
            'offset_y':     _('Y Offset'),
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
        fields = ['pressure','frequency']
        widgets = {
            'pressure'         : forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency'   : forms.NumberInput(attrs={'class': 'form-control'}),

        }
