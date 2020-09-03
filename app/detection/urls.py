from django.urls import path
from .views import Capture_View,Hdr_View, Detection_Homming
urlpatterns = [
    path('capture/', Capture_View.as_view(), name='capture'),
    path('hdr/', Hdr_View.as_view(), name='hdr'),
    path('detection-setuphomming/', Detection_Homming.as_view(), name='detection_homming')
]
