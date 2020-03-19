from django.urls import path
from connection.views import Connection_test, IsConnected
urlpatterns = [
    path('connection/', Connection_test.as_view(), name='connection'),
    path('isconnected/', IsConnected.as_view(), name='isconnected'),
    path('', Connection_test.as_view(), name='test'),
]
