from django.forms import ModelForm
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from detection.models import Images_Db

class TrackDetectionForm(forms.ModelForm):
    class Meta:
        model = TrackDetection_Db
        fields = '__all__'


class PlotOnChromatogramsForm(forms.ModelForm):
    class Meta:
        model = PlotOnChromatograms_Db
        exclude = ['image', 'track_detection']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Images_Db
        fields = '__all__'


class TrackSortForm(forms.ModelForm):
    class Meta:
        model = TrackSort_Db
        fields = ['rf']

    def clean_rf_value(self):
        try:
            rf_value = float(self.cleaned_data['rf'])
        except ValueError:
            ValidationError("Must be a number")
        if rf_value > 1 or rf_value < 0:
            ValidationError("Rf must be between 0 and 1 ")
        else:
            return float(rf_value)


class PCAAnalysisForm(forms.ModelForm):
    class Meta:
        model = PCAAnalysis_Db
        fields = ['reference',]


class HeatmapForm(forms.ModelForm):
    class Meta:
        model = Heatmap_Db
        fields = ['reference',]


class HCAAnalysisForm(forms.ModelForm):
    class Meta:
        model = HCAAnalysis_Db
        fields = ['reference','num_clusters']
