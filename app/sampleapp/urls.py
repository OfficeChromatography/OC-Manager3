from django.urls import path
from .views import Sample,SampleAppPlay,SampleAppSaveAndLoad,CalcVol

urlpatterns = [
    path('sample/', Sample.as_view(), name='sample'),
    path('samplesave/', SampleAppSaveAndLoad.as_view(), name='samplesaveandload'),
    path('sampleapp/', SampleAppPlay.as_view(), name='sampleplay'),
    path('samplecalc/', CalcVol.as_view(), name='samplecalc'),
]
