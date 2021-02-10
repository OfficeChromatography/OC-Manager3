from django.urls import path
from .views import *

urlpatterns = [
    path('sample/', SampleView.as_view(), name='sample'),
    path('sample/list/', SampleList.as_view(), name='samplelist'),


    path('sample/load/<int:id>/', SampleDetails.as_view(), name='samplelist'),
    path('sample/save/', SampleDetails.as_view(), name='samplelist'),

    path('sample/start/', SampleAppPlay.as_view(), name='sampleplay'),
    path('samplecalc/', CalcVol.as_view(), name='samplecalc'),
]
