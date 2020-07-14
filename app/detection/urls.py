from django.urls import path
from .views import Capture_View,Hdr_View
urlpatterns = [
    path('capture/', Capture_View.as_view(), name='capture'),
    path('hdr/', Hdr_View.as_view(), name='hdr'),
]
