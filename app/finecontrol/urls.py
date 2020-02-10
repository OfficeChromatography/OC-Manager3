from django.urls import path
from finecontrol import views
from finecontrol.views import MotorControl_test
urlpatterns = [
    path('/motorcontrol/', views.motorcontrol_view, name='motorcontrol'),
    path('', MotorControl_test.as_view(), name='test1')
]
