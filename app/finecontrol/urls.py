from django.urls import path
from .views import *
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('clean/', Clean.as_view(), name='pumpcontrol'),
    path('cleanprocess/', CleanControl.as_view(), name='cleanprocess'),
    path('staticpurge/', StaticPurge.as_view(), name='staticpurge'),
    path('gcode-editor/',GcodeEditor.as_view(), name='gcodeeditor'),
    # path('setuphomming/', HommingSetup.as_view(), name='homming'),
    path('syringeload/', SyringeLoad.as_view(), name='syringeload'),
    path('temperature/', Temperature.as_view(), name='temperature'),
    path('tempControl/', TempControl.as_view(), name='tempcontrol'),
    path('fan/', Fan.as_view(), name='fan'),
    path('oclab/control/', OcLabControl.as_view(), name='oclabcontrol'),

    path('export/<int:id>/', Export.as_view(), name='export'),

    path('nozzletest/', NozzleTest.as_view(), name='nozzletest'),
    path('nozzletest/list/', NozzleTestList.as_view(), name='nozzletestlist'),
    path('nozzletest/load/<int:id>/', NozzleTestDetails.as_view(), name='nozzletestload'),
    path('nozzletest/save/', NozzleTestDetails.as_view(), name='nozzletestsave'),
    path('nozzletest/delete/<int:id>/', NozzleTestDetails.as_view(), name='nozzletestdelete'),
    path('nozzletest/start/', NozzleTestPlay.as_view(), name='nozzletestplay'),
]
