from django.urls import path
from .views import *
urlpatterns = [
    path('motorcontrol/', MotorControl.as_view(), name='motorcontrol'),
    path('clean/', Clean.as_view(), name='pumpcontrol'),
    path('cleanprocess/', CleanControl.as_view(), name='cleanprocess'),
    path('staticpurge/', StaticPurge.as_view(), name='staticpurge'),
    path('gcode-editor/',GcodeEditor.as_view(), name='gcodeeditor'),
    path('syringeload/', SyringeLoad.as_view(), name='syringeload'),
    path('temperature/', Temperature.as_view(), name='temperature'),
    path('tempControl/', TempControl.as_view(), name='tempcontrol'),
    path('fan/', Fan.as_view(), name='fan'),
    path('oclab/control/', OcLabControl.as_view(), name='oclabcontrol'),

    path('method/', MethodList.as_view(), name='method_list'),
    path('method/remove/<int:id>/', MethodDetail.as_view(), name='method_remove'),
    path('method/detail/<int:id>/', MethodDetail.as_view(), name='method_detail'),
    path('method/modify/<int:id>/', MethodDetail.as_view(), name='method_update'),

    path('export/<int:id>/', Export.as_view(), name='export')
]
