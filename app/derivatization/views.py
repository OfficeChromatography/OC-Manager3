from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json
from finecontrol.calculations.DevCalc import calculateDevelopment
from finecontrol.forms import data_validations, data_validations_and_save, Method_Form
from finecontrol.models import Method_Db

class DerivatizationView(FormView):
    def get(self, request):
        """Manage the HTML view in Derivatization"""
        return render(request, 'derivatization.html', {})


class DerivatizationDetail(View):
    def delete(self, request, id):
        Method_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        method = Method_Db.objects.get(pk=id_object)

        if not Derivatization_Db.objects.filter(method=method):
            response.update({"filename":getattr(method,"filename")})
            response.update({"id":id_object})
        else:

            dev_config = Derivatization_Db.objects.get(method=method)
            response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id",]))
            response.update(model_to_dict(method))

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        id = request.POST.get("selected-element-id")

        
        if not id or not Derivatization_Db.objects.filter(method=Method_Db.objects.get(pk=id)):
            development_form = Derivatization_Form(request.POST)
            if development_form.is_valid():
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                method_form = Method_Form(request.POST)

                if not id:
                    method = method_form.save(commit=False)
                    method.auth = request.user
                    method.save()
                else:
                    method = Method_Db.objects.get(pk=id)
                development_instance.method = method
                development_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=DerivatizationBandSettings_Form(request.POST),
                )
                development_instance.pressure_settings.add(objects_save["pressure_settings"])
                development_instance.plate_properties.add(objects_save["plate_properties"])
                development_instance.zero_properties.add(objects_save["zero_position"])
                development_instance.band_settings.add(objects_save["band_settings"])

        else:
            method = Method_Db.objects.get(pk=id)
            method_form = Method_Form(request.POST, instance=method)
            method_form.save()
            development_instance = Derivatization_Db.objects.get(method=method)
            development_form = Derivatization_Form(request.POST, instance=development_instance)
            dev_inst = development_form.save(commit=False)
            dev_inst.method = method
            dev_inst.save()
            data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                          instance=development_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=development_instance.pressure_settings.get()),
                    zero_position=ZeroPosition_Form(request.POST,
                                                    instance=development_instance.zero_properties.get()),
                    band_settings=DerivatizationBandSettings_Form(request.POST,
                                                               instance=development_instance.band_settings.get()),
                )
            

        return JsonResponse({'message':'Data !!'})


class DerivatizationAppPlay(View):
        def post(self, request):
            
            forms_data = data_validations( plate_properties=PlateProperties_Form(request.POST),
                                            pressure_settings=PressureSettings_Form(request.POST),
                                            zero_position=ZeroPosition_Form(request.POST),
                                            band_settings=DevelopmentBandSettings_Form(request.POST))

            gcode = calculateDerivatization(forms_data)
            OC_LAB.print_from_list(gcode)
            return JsonResponse({'error': 'f.errors'})

# AUX Functions

def data_validations(**kwargs):
    # Iterate each form and run validations
    forms_data = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            forms_data.update(form.cleaned_data)
        else:
            print(f'Error on {key_form}')
            return
    return forms_data


def data_validations_and_save(**kwargs):
    objects_saved = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            objects_saved[key_form] = form.save()
        else:
            print(form.errors)
            return JsonResponse({'error':f'Check {key_form}'})
    return objects_saved
