from django.forms import ModelForm
from django import forms
from .models import *



# class MovementSettings_Form(forms.ModelForm):
#     class Meta:
#         model = MovementSettings_Db
#         fields = ['motor_speed','delta_x','delta_y']
#
#         def clean_motor_speed(self):
#             motor_speed = self.motor_speed
#             return int(motor_speed)

# class PressureSettings_Form(forms.ModelForm):
#     class Meta:
#         model = PressureSettings_Db
#         fields = ['pressure','frequency', 'temperature','nozzlediameter', "rinsingPeriod"]
#
#     def clean_temperature(self):
#         temperature = self.cleaned_data["temperature"]
#         if not temperature:
#             return 0
#         return temperature
#
#     def clean_rinsingPeriod(self):
#         rinsingPeriod = self.cleaned_data["rinsingPeriod"]
#         if not rinsingPeriod:
#             return 999999
#         return rinsingPeriod

class BandsComponents_Form(forms.ModelForm):
    class Meta:
        model = BandsComponents_Db
        fields = ['band_number','product_name','company','region','year', 'volume', 'type', 'density', 'viscosity']
        exclude = ['sample_application']

    def clean_band_number(self):
        band_number = self.cleaned_data.get("band_number")
        return band_number

    def clean_product_name(self):
        value = self.cleaned_data.get("product_name")
        return value

    def clean_company(self):
        value = self.cleaned_data.get("company")
        return value

    def clean_region(self):
        value = self.cleaned_data.get("region")
        return value

    def clean_year(self):
        value = self.cleaned_data.get("year")
        return value

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
