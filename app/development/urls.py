from .views import *
from django.urls import path
urlpatterns = [
    path('development/', DevelopmentView.as_view(), name='development'),
    path('development/list', DevelopmentList.as_view(), name='development_list'),

    path('development/load/<int:id>/', DevelopmentDetail.as_view(), name='development_element'),
    path('development/save/', DevelopmentDetail.as_view(), name='development_element'),

    path('development/start/', DevelopmentAppPlay.as_view(), name='development_element'),
]
