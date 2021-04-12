from django.urls import path
from .views import *
from finecontrol.views import MethodList

urlpatterns = [
    path('sample/', SampleView.as_view(), name='sample'),
    path('sample/list/', MethodList.as_view(), name='samplelist'),


    path('sample/load/<int:id>/', SampleDetails.as_view(), name='sampleload'),
    path('sample/save/', SampleDetails.as_view(), name='samplesave'),
    path('sample/delete/<int:id>/', SampleDelete.as_view(), name='sampledelete'),

    path('sample/start/', SampleAppPlay.as_view(), name='sampleplay'),
    path('samplecalc/', CalcVol.as_view(), name='samplecalc'),
]
