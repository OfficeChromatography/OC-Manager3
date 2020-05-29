from django.urls import path
from .views import Sample,SampleAppPlay,SampleAppSaveAndLoad, HommingSetup

urlpatterns = [
    path('sample/', Sample.as_view(), name='sample'),
    path('samplesave/', SampleAppSaveAndLoad.as_view(), name='samplesaveandload'),
    path('sampleapp/', SampleAppPlay.as_view(), name='sampleplay'),
    path('gohomming/', HommingSetup.as_view(), name='homming'),
    # path('samplestop/', SampleAppStop.as_view(), name='samplestop'),
]
