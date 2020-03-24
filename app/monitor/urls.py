# chat/urls.py
from django.urls import path
from .views import MonitorView

from . import views

urlpatterns = [
    path('monitor/', MonitorView.as_view(), name='monitor'),
]
