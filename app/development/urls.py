from .views import *
from django.urls import path
from finecontrol.views import MethodList

urlpatterns = [
    path('development/', DevelopmentView.as_view(), name='development'),
    path('development/list', MethodList.as_view(), name='development_list'),

    path('development/load/<int:id>/', DevelopmentDetail.as_view(), name='development_element'),
    path('development/save/', DevelopmentDetail.as_view(), name='development_element'),

    path('development/start/', DevelopmentAppPlay.as_view(), name='development_element'),
]
