from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from finecontrol.forms import data_validations, data_validations_and_save, \
    Method_Form
from finecontrol.models import Method_Db

import json
from types import SimpleNamespace

from .forms import *
from .models import *

from connection.forms import OC_LAB
from finecontrol.calculations.sampleAppCalc import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import Http404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from .serializers import *


class SampleView(FormView):
    def get(self, request):
        """Manage the HTML view in SampleApp"""
        return render(request, 'sample.html', {})


class SampleAppListCreate(ListCreateAPIView):
    serializer_class = SampleAppSerializer
    queryset = SampleApplication_Db.objects.all()

    def get_queryset(self):
        return SampleApplication_Db.objects.filter(
            method=self.kwargs['method_id'])


class SampleAppRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = SampleAppSerializer
    queryset = SampleApplication_Db.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'


class BandComponentsListCreate(ListCreateAPIView):
    serializer_class = BandComponentsSerializer
    # queryset = BandsComponents_Db.objects.all()

    def get_queryset(self):
        return BandsComponents_Db.objects.filter(
            sample_application=self.kwargs['sample_id'])


class SampleAppPlay(View):
    def post(self, request):
        # Run the form validations and return the clean data
        forms_data = data_validations(
            plate_properties=PlateProperties_Form(request.POST),
            pressure_settings=PressureSettings_Form(request.POST),
            zero_position=ZeroPosition_Form(request.POST),
            band_settings=BandSettings_Form(request.POST),
            movement_settings=MovementSettings_Form(request.POST))

        bands_components = json.loads(request.POST.get('table'))
        forms_data.update({'table': bands_components})

        # With the data, gcode is generated
        gcode = calculate(forms_data)

        # Printrun
        OC_LAB.print_from_list(gcode)
        return JsonResponse({'error': 'f.errors'})


class CalcVol(APIView):
    def post(self, request):
        serializer = BandComponentsSerializer(data=request.data['table'], many=True)
        if serializer.is_valid():
            print(serializer.data)
        else:
            print(serializer.errors)
#         results = calculate_volume_application_info(data)
        return JsonResponse({'results': 'results'})
