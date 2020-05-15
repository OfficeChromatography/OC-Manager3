from django.urls import path
from .views import MotorControl, PumpControl,CleanControl
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('pumpcontrol/', PumpControl.as_view(), name='pumpcontrol'),
    path('cleanprocess/', CleanControl.as_view(), name='cleanprocess'),
]
