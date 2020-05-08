from django.urls import path
from sampleapp.views import Sample,SampleAppPlay

urlpatterns = [
    path('sample2/', Sample.as_view(), name='sample'),
    # path('samplesave/', SampleAppSaveAndLoad.as_view(), name='samplesaveandload'),
    path('sampleapp2/', SampleAppPlay.as_view(), name='sampleplay'),
    # path('samplestop/', SampleAppStop.as_view(), name='samplestop'),
]
