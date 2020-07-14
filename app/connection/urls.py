from django.urls import path
from connection.views import Connection_test, IsConnected, CommunicationWithOC
urlpatterns = [
    path('connection/', Connection_test.as_view(), name='connection'),
    path('isconnected/', IsConnected.as_view(), name='isconnected'),
    path('', Connection_test.as_view(), name='test'),
    path('send/', CommunicationWithOC.as_view(), name='test'),
]
