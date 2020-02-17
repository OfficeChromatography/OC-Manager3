# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.monitor, name='monitor'),
    path('<str:room_name>/', views.room, name='room'),
]
