from django.urls import path
from .views import MotorControl, PumpControl, CleanControl, GcodeEditor
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('pumpcontrol/', PumpControl.as_view(), name='pumpcontrol'),
    path('cleanprocess/', CleanControl.as_view(), name='cleanprocess'),
    path('gcode-editor/',GcodeEditor.as_view(), name='gcodeeditor')
]
