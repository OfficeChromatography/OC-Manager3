from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import Development_Form, PlateProperties_Form, DevelopmentBandSettings_Form, PressureSettings_Form, Flowrate_Form
from .models import *#Development_Db, BandSettings_Dev_Db, PlateProperties_Dev_Db, PressureSettings_Dev_Db, flowrate_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
from printrun import printcore, gcoder

import json
from decimal import *

from finecontrol.forms import ZeroPosition_Form
from finecontrol.models import ZeroPosition


from finecontrol.calculations.DevCalc import calculateDevelopment

forms = {
    'Development_Form': Development_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'DevelopmentBandSettings_Form': DevelopmentBandSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    'ZeroPosition_Form': ZeroPosition_Form(),
    'Flowrate_Form': Flowrate_Form(),
    }

class Development(FormView):
    def get(self, request):
        if 'LISTLOAD' in request.GET:
            development = Development_Db.objects.filter(auth=request.user).order_by('-id')
            names = [i.file_name for i in development]
            return JsonResponse(names, safe=False)
        else:
            forms['list_load'] = Development_Db.objects.filter(auth=request.user).order_by('-id')
            #print(forms['list_load'])
            return render(request,'development.html',forms)

class DevelopmentPlay(View):
    def post(self, request):
        #print(request.POST)
        # Treatment for play button
        if 'START' in request.POST:
            if OC_LAB.paused == True:
                OC_LAB.resume()
            else:
                # Run the form validations and return the clean data
                forms_data = data_validations(   plate_properties_form    =   PlateProperties_Form(request.POST),
                                    pressure_settings_form   =   PressureSettings_Form(request.POST),
                                    zero_position_form       =   ZeroPosition_Form(request.POST))

                forms_data.update(json.loads(request.POST.get('devBandSettings')))
                forms_data.update(json.loads(request.POST.get('flowrate')))
                
                # With the data, gcode is generated
                gcode = calculateDevelopment(forms_data)

                # Printrun
                OC_LAB.print_from_list(gcode)
                return JsonResponse({'error':'f.errors'})
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message':'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message':'paused'})

class DevelopmentSaveAndLoad(View):
    def post(self, request):
        development_form  =   Development_Form(request.POST, request.user)
        plate_properties_form    =   PlateProperties_Form(request.POST)
        pressure_settings_form = PressureSettings_Form(request.POST)
        #developmentBandSettings_form       =   DevelopmentBandSettings_Form(request.POST)
        zero_position_form       =   ZeroPosition_Form(request.POST)

        devBandSettings = request.POST.get('devBandSettings')
        devBandSettings_data = json.loads(devBandSettings)

        flowrateSettings = request.POST.get('flowrate')
        flowrateSettings_data = json.loads(flowrateSettings)
        print(flowrateSettings_data)
        
        # Check Plate Property Formular
        if plate_properties_form.is_valid():
            plate_properties_object = plate_properties_form.save()
        else:
            return JsonResponse({'error':'Check plate properties'})

        # Check Band Settings Formular
        developmentBandSettings_form = DevelopmentBandSettings_Form(devBandSettings_data)
        if developmentBandSettings_form.is_valid():
            developmentBandSettings_object = developmentBandSettings_form.save()
        else:
            return JsonResponse({'error':'Check band properties'})

        # Check Pressure Settings Formular
        if pressure_settings_form.is_valid():
            pressure_settings_object = pressure_settings_form.save()
        else:
            print(pressure_settings_form)
            return JsonResponse({'error':'Check pressure settings'})
            
        # Check Home Settings Formular
        if zero_position_form.is_valid():
            zero_position_object = zero_position_form.save()
        else:
            return JsonResponse({'error':'Check home settings'})

        #Check flowrate Settings Form
        flowrate_form = Flowrate_Form(flowrateSettings_data)
        if flowrate_form.is_valid():
            flowrate_object = flowrate_form.save()
        else:
            return JsonResponse({'error':'Check flowrate settings'})

        # If everything is OK then it checks the name and tries to save the Complete Sample App
        if development_form.is_valid():
            filename = development_form.cleaned_data['file_name']
            in_db=Development_Db.objects.filter(file_name=filename).filter(auth_id=request.user)

            # Check if theres
            if len(in_db)>0:
                return JsonResponse({'error':'File Name exist!'})
            else:
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                development_instance.pressure_settings = pressure_settings_object
                development_instance.plate_properties = plate_properties_object
                development_instance.developmentBandSettings = developmentBandSettings_object
                development_instance.zero_position = zero_position_object
                development_instance.flowrate = flowrate_object
                new_development=development_instance.save()

                return JsonResponse({'message':f'The File {filename} was saved!'})

        else:
            return JsonResponse({'error':'Please fill the filename!'})

    def get(self, request):
        file_name=request.GET.get('filename')

        
        development_conf=model_to_dict(Development_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Dev_Db.objects.get(id=development_conf['plate_properties']))
        developmentBandSettings_conf=model_to_dict(BandSettings_Dev_Db.objects.get(id=development_conf['developmentBandSettings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Dev_Db.objects.get(id=development_conf['pressure_settings']))
        zero_position_conf=model_to_dict(ZeroPosition.objects.get(id=development_conf['zero_position']))
        flowrate_conf=model_to_dict(Flowrate_Db.objects.get(id=development_conf['flowrate']))

        development_conf.update(plate_properties_conf)
        development_conf.update(developmentBandSettings_conf)
        development_conf.update(pressure_settings_conf)
        development_conf.update(zero_position_conf)
        development_conf.update(flowrate_conf)
        
        return JsonResponse(development_conf)

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


