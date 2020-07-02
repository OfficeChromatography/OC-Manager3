from .views import Development,DevelopmentPlay,DevelopmentSaveAndLoad, HommingSetup
from django.urls import path
urlpatterns = [
    path('development/', Development.as_view(), name='development'),
    path('developmentsave/', DevelopmentSaveAndLoad.as_view(), name='developmentsaveandload'),
    path('developmentplay/', DevelopmentPlay.as_view(), name='developmentplay'),
    path('gohomming/', HommingSetup.as_view(), name='homming'),
    # path('samplestop/', SampleAppStop.as_view(), name='samplestop'),
]
