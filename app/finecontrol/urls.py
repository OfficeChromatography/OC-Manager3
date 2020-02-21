from django.urls import path
from .views import MotorControl, PumpControl
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('pumpcontrol/', PumpControl.as_view(), name='pumpcontrol'),
]
