from django.urls import path
from connection.views import Connection_test
urlpatterns = [
    path('/connection/', Connection_test.as_view(), name='connection'),
    path('', Connection_test.as_view(), name='test'),
]
