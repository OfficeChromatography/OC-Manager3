from django.urls import path
from .views import MotorControl
urlpatterns = [
    path('/motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
]
