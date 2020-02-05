from django.urls import path
from finecontrol.views import MotorControl_test
urlpatterns = [
    path('/motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
]
