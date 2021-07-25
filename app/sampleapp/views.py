from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from finecontrol.forms import data_validations, data_validations_and_save, Method_Form
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
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import *

class SampleView(FormView):
    def get(self, request):
        """Manage the HTML view in SampleApp"""
        return render(request,'sample.html',{})

class SampleAppListCreate(ListCreateAPIView):
    serializer_class = SampleAppSerializer
    queryset = SampleApplication_Db.objects.all()

class SampleAppDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = SampleAppSerializer
    queryset = SampleApplication_Db.objects.all()
    lookup_url_kwarg = 'id'


# class SampleList(FormView):

#     def get(self, request):
#         """Returns a list with all the SampleApplications save in DB"""
#         sample_application = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
#         data_saved = [[i.filename,i.id] for i in sample_application]
#         return JsonResponse(data_saved, safe=False)

class SampleDelete(View):

    def delete(self, request, id):
        apps = SampleApplication_Db.objects.filter(method=Method_Db.objects.get(pk=id))
        apps.delete()
        return JsonResponse({})

class SampleDetails(View):

    def delete(self, request, id):
        Method_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        method = Method_Db.objects.get(pk=id_object)
        if not SampleApplication_Db.objects.filter(method=method):
            response.update({"filename":getattr(method,"filename")})
            response.update({"id":id_object})
        else:
            
            sample_config = SampleApplication_Db.objects.get(method=method)
            response.update(model_to_dict(sample_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.band_settings.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.zero_properties.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.movement_settings.get(), exclude=["id",]))
            response.update(model_to_dict(method))

            bands_components = BandsComponents_Db.objects.filter(sample_application=sample_config.id).values()
            response.update({'bands_components': [entry for entry in bands_components]})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        id = request.POST.get("selected-element-id")
        bands_components = json.loads(request.POST.get('table'))
        
        if not id or not SampleApplication_Db.objects.filter(method=Method_Db.objects.get(pk=id)):
            sample_form = SampleApplication_Form(request.POST)
            if sample_form.is_valid():
                sample_instance = sample_form.save(commit=False)
                sample_instance.auth = request.user
                method_form = Method_Form(request.POST)
                
                if not id:
                    method = method_form.save(commit=False)
                    method.auth = request.user
                    method.save()
                else:
                    method = Method_Db.objects.get(pk=id)
                sample_instance.method = method
                sample_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=BandSettings_Form(request.POST),
                    movement_settings=MovementSettings_Form(request.POST),
                )
                sample_instance.pressure_settings.add(objects_save["pressure_settings"])
                sample_instance.plate_properties.add(objects_save["plate_properties"])
                sample_instance.zero_properties.add(objects_save["zero_position"])
                sample_instance.band_settings.add(objects_save["band_settings"])
                sample_instance.movement_settings.add(objects_save["movement_settings"])
                

        else:
            method = Method_Db.objects.get(pk=id)
            method_form = Method_Form(request.POST, instance=method)
            method_form.save()
            sample_instance = SampleApplication_Db.objects.get(method=method)
            sample_form = SampleApplication_Form(request.POST, instance=sample_instance)
            sample_inst= sample_form.save(commit=False)
            sample_inst.method = method
            sample_inst.save()
            data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                            instance=sample_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=sample_instance.pressure_settings.get()),
                    zero_position=ZeroPosition_Form(request.POST,
                                                            instance=sample_instance.zero_properties.get()),
                    band_settings=BandSettings_Form(request.POST,
                                                            instance=sample_instance.band_settings.get()),
                    movement_settings=MovementSettings_Form(request.POST, instance=sample_instance.movement_settings.get()),
                )
            sample_instance.band_components.all().delete()

        for band_component in bands_components:
            band_component_form = BandsComponents_Form(band_component)
            if band_component_form.is_valid():
                band_component_object = band_component_form.save()
                sample_instance.band_components.add(band_component_object)

        return JsonResponse({'message':'Data !!'})

class SampleAppPlay(View):
    def post(self, request):
        # Run the form validations and return the clean data
        forms_data = data_validations(
            plate_properties=PlateProperties_Form(request.POST),
            pressure_settings=PressureSettings_Form(request.POST),
            zero_position=ZeroPosition_Form(request.POST),
            band_settings=BandSettings_Form(request.POST),
            movement_settings=MovementSettings_Form(request.POST)
        )

        bands_components = json.loads(request.POST.get('table'))
        forms_data.update({'table': bands_components})

        # With the data, gcode is generated
        gcode = calculate(forms_data)

        # Printrun
        OC_LAB.print_from_list(gcode)
        return JsonResponse({'error':'f.errors'})


class CalcVol(View):
    def post(self, request):
        forms_data = data_validations(  plate_properties_form    =   PlateProperties_Form(request.POST),
                                        band_settings_form       =   BandSettings_Form(request.POST),
                                        movement_settings_form   =   MovementSettings_Form(request.POST),
                                        pressure_settings_form   =   PressureSettings_Form(request.POST),
                                        zero_position_form       =   ZeroPosition_Form(request.POST))
        forms_data.update({'table':json.loads(request.POST.get('table'))})
        data = SimpleNamespace(**forms_data)
        results = calculate_volume_application_info(data)
        return JsonResponse({'results':results})
