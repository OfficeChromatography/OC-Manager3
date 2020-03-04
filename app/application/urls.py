from django.urls import path
from application.views import Sample

urlpatterns = [
    path('sample/', Sample.as_view(), name='motorcontrol'),
]
