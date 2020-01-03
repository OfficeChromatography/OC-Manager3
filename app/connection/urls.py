from django.urls import path
from connection import views

urlpatterns = [
    path('/connection/', views.connection_view, name='connection'),
    

]
