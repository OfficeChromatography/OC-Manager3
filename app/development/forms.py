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
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['size_y'] = 100
        initial['size_x'] = 100
        initial['offset_left'] = 1
        initial['offset_right'] = 1
        initial['offset_top'] = 1
        initial['offset_bottom'] = 50
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
            'offset_bottom' : forms.Select(attrs={'class': 'form-control'}, choices=[(2.5,2.5),(50,50)]),
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
        initial['volume'] = 100
        initial['fluid'] = 'Methanol'
        kwargs['initial'] = initial
        super(DevelopmentBandSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = BandSettings_Dev_Db
        fields = ['volume','fluid','printBothways','density','viscosity']
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
        }
        labels = {
            'volume'         : _('Volume'),
            'fluid'         : _('Fluid'),
        }

        def clean(self):
            fluid = self.cleaned_data.get("fluid")
            density = self.cleaned_data.get("density")
            viscosity = self.cleaned_data.get("viscosity")
            print('helloforms')
            if fluid == 'Specific':
                if density == "null" or viscosity == "null":
                    raise forms.ValidationError(
                        "Specify Density and Viscosity!"
                    )
            return self.cleaned_data
            

class MovementSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['motor_speed'] = 3000
        initial['delta_x'] = 0.5
        kwargs['initial'] = initial
        super(MovementSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = MovementSettings_Dev_Db
        fields = ['motor_speed','delta_x']
        widgets = {
            'motor_speed'   : forms.NumberInput(attrs={'class': 'form-control'}),
            'delta_x'       : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'motor_speed' : _('MotorSpeed'),
            'delta_x'     : _('Delta X'),
        }

        def clean_motor_speed(self):
            motor_speed = self.motor_speed
            return int(motor_speed)


class PressureSettings_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['pressure'] = 21
        initial['frequency'] = 1400
        initial['temperature'] = 0
        kwargs['initial'] = initial
        super(PressureSettings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = PressureSettings_Dev_Db
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
