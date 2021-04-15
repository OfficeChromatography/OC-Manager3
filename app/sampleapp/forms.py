from django.forms import ModelForm
from django import forms
from .models import *


class SampleApplication_Form(forms.ModelForm):
    class Meta:
        model = SampleApplication_Db
        fields = ['filename','method']

class PlateProperties_Form(forms.ModelForm):
    class Meta:
        model = PlateProperties_Db
        fields = ['size_x','size_y','offset_left','offset_right','offset_top','offset_bottom']


class BandSettings_Form(forms.ModelForm):
    class Meta:
        model = BandSettings_Db
        fields = ['main_property','value','height','gap','waitTime']

        def clean_main_property(self):
            return int(self.main_property)


class MovementSettings_Form(forms.ModelForm):
    class Meta:
        model = MovementSettings_Db
        fields = ['motor_speed','delta_x','delta_y']

        def clean_motor_speed(self):
            motor_speed = self.motor_speed
            return int(motor_speed)

class PressureSettings_Form(forms.ModelForm):
    class Meta:
        model = PressureSettings_Db
        fields = ['pressure','frequency', 'temperature','nozzlediameter']

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

class ZeroPosition_Form(forms.ModelForm):

    class Meta:
        model = ZeroPosition_Db
        fields = ['zero_x','zero_y']
