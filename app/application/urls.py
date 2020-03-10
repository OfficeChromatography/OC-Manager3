from django.urls import path
from application.views import Sample, Sample_Save

urlpatterns = [
    path('sample/', Sample.as_view(), name='sample'),
    path('samplesave/', Sample_Save.as_view(), name='samplesave'),
]
