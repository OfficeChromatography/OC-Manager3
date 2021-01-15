from .views import *
from django.urls import path
urlpatterns = [
    path('development/', DevelopmentView.as_view(), name='development'),
    path('development/list', DevelopmentList.as_view(), name='development_list'),

    path('development/load/<int:id>/', DevelopmentDetail.as_view(), name='development_element'),
    path('development/save/', DevelopmentDetail.as_view(), name='development_element'),


    path('developmentsave/', DevelopmentSaveAndLoad.as_view(), name='developmentsaveandload'),
    path('developmentplay/', DevelopmentPlay.as_view(), name='developmentplay'),
    # path('gohomming/', HommingSetup.as_view(), name='homming'),
    # path('developmentcalc/', DevelopmentCalc.as_view(), name='developmentcalc'),
    # path('samplestop/', SampleAppStop.as_view(), name='samplestop'),
]
