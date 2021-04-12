from django.forms import ModelForm
from django import forms
from .models import *


class Derivatization_Form(forms.ModelForm):
    class Meta:
        model = Derivatization_Db
        fields = ['filename', 'method']

class PlateProperties_Form(forms.ModelForm):

    class Meta:
        model = PlateProperties_Db
        fields = ['size_x','size_y','offset_left','offset_right','offset_top','offset_bottom']

class DerivatizationBandSettings_Form(forms.ModelForm):

    # printBothways = forms.BooleanField()

    class Meta:
        model = BandSettings_Der_Db
        fields = ['volume', 'applications', 'printBothways','waitTime', 'description']

    def clean(self):
        if self.cleaned_data.get('printBothways'):
            self.cleaned_data['printBothways']="True"
        else:
            self.cleaned_data['printBothways']="False"
        return self.cleaned_data

class PressureSettings_Form(forms.ModelForm):

       class Meta:
        model = PressureSettings_Der_Db
        fields = ['temperature','nozzlediameter','pressure','motor_speed']

class ZeroPosition_Form(forms.ModelForm):

    class Meta:
        model = ZeroPosition_Db
        fields = ['zero_x','zero_y']