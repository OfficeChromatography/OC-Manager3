from django.urls import path
from connection import views
from connection.views import Connection_test
urlpatterns = [
    path('/connection/', Connection_test.as_view(), name='connection'),
    path('', Connection_test.as_view(), name='test'),
    # path('/2/', Test_view.as_view(), name='test'),
]
