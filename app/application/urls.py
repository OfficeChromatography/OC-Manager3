from django.urls import path
from application.views import Sample, Sample_EndPoint

urlpatterns = [
    path('sample/', Sample.as_view(), name='sample'),
    path('samplesave/', Sample_EndPoint.as_view(), name='samplesave'),
]
