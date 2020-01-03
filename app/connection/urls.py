from django.urls import path
from connection import views

urlpatterns = [
    path('', views.connection_view, name='connection'),


]
