from django.urls import path
from .views import MotorControl, Clean, CleanControl, GcodeEditor, HommingSetup, StaticPurge
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('clean/', Clean.as_view(), name='pumpcontrol'),
    path('cleanprocess/', CleanControl.as_view(), name='cleanprocess'),
    path('staticpurge/', StaticPurge.as_view(), name='staticpurge'),
    path('gcode-editor/',GcodeEditor.as_view(), name='gcodeeditor'),
    path('setuphomming/', HommingSetup.as_view(), name='homming'),
]
