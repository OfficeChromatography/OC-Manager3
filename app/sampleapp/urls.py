from django.urls import path
from .views import *
from finecontrol.views import MethodList

urlpatterns = [
    path('sample/', SampleView.as_view(), name='sample'),

    path('sample/start/', SampleAppPlay.as_view(), name='sampleplay'),
    path('sample/calcvol/', CalcVol.as_view(), name='samplecalc'),

    path('sample/band_components/<int:sample_id>/',
         BandComponentsListCreate.as_view(), name='bandComponentsList'),

    path('sample/list/<int:method_id>/', SampleAppListCreate.as_view(), name='sampleAppList'),
    path('sample/create/', SampleAppListCreate.as_view(), name='sampleAppCreate'),
    path('sample/detail/<int:id>/', SampleAppRetrieveUpdateDestroy.as_view(), name='sampleAppDetail'),
    path('sample/remove/<int:id>/', SampleAppRetrieveUpdateDestroy.as_view(), name='sampleAppRemove'),
    path('sample/modify/<int:id>/', SampleAppRetrieveUpdateDestroy.as_view(), name='sampleAppModify'),



]
