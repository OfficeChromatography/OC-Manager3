from .views import DevelopmentControl
from django.urls import path
urlpatterns = [
    path('development/', DevelopmentControl.as_view(), name='development'),
]
