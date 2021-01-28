from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json
from finecontrol.calculations.DevCalc import calculateDevelopment

class DevelopmentView(FormView):
    def get(self, request):
        """Manage the HTML view in Development"""
        return render(request, 'development.html', {})


class DevelopmentList(FormView):

    def get(self, request):
        """Returns a list with all the SampleApplications save in DB"""
        developments = Development_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = [[development.filename, development.pk] for development in developments]
        return JsonResponse(data_saved, safe=False)

class DevelopmentDetail(View):
    def delete(self, request, id):
        Development_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        dev_config = Development_Db.objects.get(pk=id_object)

        response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config))

        flowrate_entry = Flowrate_Db.objects.filter(development=id_object).values('value')
        response.update({'flowrate': [entry for entry in flowrate_entry]})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        id = request.POST.get("selected-element-id")

        flowrate = request.POST.get('flowrate')
        flowrate = json.loads(flowrate)

        if not id:
            development_form = Development_Form(request.POST)
            if development_form.is_valid():
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                development_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=DevelopmentBandSettings_Form(request.POST),
                )
                development_instance.pressure_settings.add(objects_save["pressure_settings"])
                development_instance.plate_properties.add(objects_save["plate_properties"])
                development_instance.zero_properties.add(objects_save["zero_position"])
                development_instance.band_settings.add(objects_save["band_settings"])

        else:
            development_instance = Development_Db.objects.get(pk=id)
            development_form = Development_Form(request.POST, instance=development_instance)
            development_form.save()
            data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                          instance=development_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=development_instance.pressure_settings.get()),
                    zero_position=ZeroPosition_Form(request.POST,
                                                    instance=development_instance.zero_properties.get()),
                    band_settings=DevelopmentBandSettings_Form(request.POST,
                                                               instance=development_instance.band_settings.get()),
                )
            development_instance.flowrates.all().delete()

        for flow_value in flowrate:
            flowrate_form = Flowrate_Form(flow_value)
            if flowrate_form.is_valid():
                flowrate_object = flowrate_form.save()
                development_instance.flowrates.add(flowrate_object)

        return JsonResponse({'message':'Data !!'})


class DevelopmentAppPlay(View):
        def post(self, request):
            flowrates = json.loads(request.POST.get('flowrate'))
            forms_data = data_validations( plate_properties=PlateProperties_Form(request.POST),
                                            pressure_settings=PressureSettings_Form(request.POST),
                                            zero_position=ZeroPosition_Form(request.POST),
                                            band_settings=DevelopmentBandSettings_Form(request.POST))

            forms_data['flowrate'] = flowrates
            gcode = calculateDevelopment(forms_data)
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
