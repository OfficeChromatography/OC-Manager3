from django.urls import path
from finecontrol import views

urlpatterns = [
    path('/motorcontrol/', views.motorcontrol_view, name='motorcontrol'),
]
