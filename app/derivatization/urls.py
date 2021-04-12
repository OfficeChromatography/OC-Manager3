from .views import *
from django.urls import path
from finecontrol.views import MethodList

urlpatterns = [
    path('derivatization/', DerivatizationView.as_view(), name='derivatization'),
    path('derivatization/list', MethodList.as_view(), name='derivatization_list'),

    path('derivatization/load/<int:id>/', DerivatizationDetail.as_view(), name='derivatization_element'),
    path('derivatization/save/', DerivatizationDetail.as_view(), name='derivatization_element'),
    path('derivatization/delete/<int:id>/', DerivatizationDelete.as_view(), name='derivatizationdelete'),

    path('derivatization/start/', DerivatizationAppPlay.as_view(), name='derivatization_element'),
]