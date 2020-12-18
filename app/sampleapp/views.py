from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
import json
import numpy as np
import math
from types import SimpleNamespace

from .forms import *
from .models import *

from finecontrol.forms import ZeroPosition_Form
from finecontrol.models import ZeroPosition
from connection.forms import OC_LAB
from finecontrol.gcode.GcodeGenerator import GcodeGenerator
from finecontrol.calculations.sampleAppCalc import *



forms = {
    'SampleApplication_Form': SampleApplication_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'BandSettings_Form': BandSettings_Form(),
    'MovementSettings_Form': MovementSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    'BandComponents_Form':BandsComponents_Form(),
    'ZeroPosition_Form': ZeroPosition_Form()
    }

class Table(View):
    def get(self, request):
        return render(request,'modules/sampleapp/table/row.html')

class SampleList(FormView):
    def get(self, request):
        """Returns a list with all the SampleApplications save in DB"""
        sample_application = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = [[i.file_name,i.id] for i in sample_application]
        return JsonResponse(data_saved, safe=False)

class SampleView(FormView):
    def get(self, request):
        forms['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
        return render(request,'sample.html',forms)

class SampleDetails(View):
    def get(self, request, id):
        id_object=id
        sample_application_conf=model_to_dict(SampleApplication_Db.objects.filter(pk=id_object).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Db.objects.get(id=sample_application_conf['plate_properties']))
        band_settings_conf=model_to_dict(BandSettings_Db.objects.get(id=sample_application_conf['band_settings']))
        movement_settings_conf=model_to_dict(MovementSettings_Db.objects.get(id=sample_application_conf['movement_settings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Db.objects.get(id=sample_application_conf['pressure_settings']))
        zero_position_conf=model_to_dict(ZeroPosition.objects.get(id=sample_application_conf['zero_position']))
        bands_components = BandsComponents_Db.objects.filter(sample_application=SampleApplication_Db.objects.filter(pk=id_object).filter(auth_id=request.user)[0])

        bands=dict()
        for i, band in enumerate(bands_components):
            bands[i]=model_to_dict(band)
        bands = {'bands':bands}
        sample_application_conf.update(bands)
        sample_application_conf.update(plate_properties_conf)
        sample_application_conf.update(band_settings_conf)
        sample_application_conf.update(movement_settings_conf)
        sample_application_conf.update(pressure_settings_conf)
        sample_application_conf.update(zero_position_conf)
        print(f'Property id:{id_object} of sample app loaded!')
        return JsonResponse(sample_application_conf)

    def post(self, request):
        # Check the data receive and save it
        sample_application_form  =   SampleApplication_Form(request.POST, request.user)
        objects_save = data_validations_and_save(
            plate_properties    =   PlateProperties_Form(request.POST),
            band_settings       =   BandSettings_Form(request.POST),
            movement_settings   =   MovementSettings_Form(request.POST),
            pressure_settings   =   PressureSettings_Form(request.POST),
            zero_position       =   ZeroPosition_Form(request.POST)

        )
        print(request.POST)
        table_data = json.loads(request.POST.get('table'))
        # If everything is OK then it checks the name and tries to save the Complete Sample App
        if sample_application_form.is_valid():
            filename = sample_application_form.cleaned_data['file_name']
            in_db=SampleApplication_Db.objects.filter(file_name=filename).filter(auth_id=request.user)
            # Check if theres
            if len(in_db)>0:
                in_db[0].movement_settings = objects_save['movement_settings']
                in_db[0].pressure_settings = objects_save['pressure_settings']
                in_db[0].plate_properties = objects_save['plate_properties']
                in_db[0].band_settings = objects_save['band_settings']
                in_db[0].zero_position = objects_save['zero_position']
                in_db[0].save()
                BandsComponents_Db.objects.filter(sample_application=in_db[0]).delete()
                for i in table_data:
                    # Format data
                    i['band_number'] = i['band']
                    i['volume'] = i['volume (ul)']

                    bands_components_form = BandsComponents_Form(i)

                    if bands_components_form.is_valid():
                        bands_components_instance = bands_components_form.save(commit=False)
                        bands_components_instance.sample_application = in_db[0]
                        bands_components_instance.save()
                    else:
                        JsonResponse({'error':bands_components_form.errors})

                return JsonResponse({'message':'Data updated!!'})
            else:
                sample_application_instance = sample_application_form.save(commit=False)
                sample_application_instance.auth = request.user
                sample_application_instance.movement_settings = objects_save['movement_settings']
                sample_application_instance.pressure_settings = objects_save['pressure_settings']
                sample_application_instance.plate_properties = objects_save['plate_properties']
                sample_application_instance.band_settings = objects_save['band_settings']
                sample_application_instance.zero_position = objects_save['zero_position']
                new_sample_application = sample_application_instance.save()


                for i in table_data:
                    # Format data
                    i['band_number'] = i['band']
                    i['volume'] = i['volume (ul)']

                    bands_components_form = BandsComponents_Form(i)

                    if bands_components_form.is_valid():
                        bands_components_instance=bands_components_form.save(commit=False)
                        bands_components_instance.sample_application = sample_application_instance
                        bands_components_instance.save()
                    else:
                        JsonResponse({'error':bands_components_form.errors})

                return JsonResponse({'message':f'The File {filename} was saved!'})
        else:
            return JsonResponse({'error':'Please fill in the filename!'})

class SampleAppPlay(View):
    def post(self, request):
        # Play button
        if 'START' in request.POST:
            if OC_LAB.paused == True:
                OC_LAB.resume()
            else:
                # Run the form validations and return the clean data
                forms_data = data_validations(  plate_properties_form    =   PlateProperties_Form(request.POST),
                                                band_settings_form       =   BandSettings_Form(request.POST),
                                                movement_settings_form   =   MovementSettings_Form(request.POST),
                                                pressure_settings_form   =   PressureSettings_Form(request.POST),
                                                zero_position_form       =   ZeroPosition_Form(request.POST))


                # Add table data
                forms_data.update({'table':json.loads(request.POST.get('table'))})

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
        results = returnDropEstimateVol(data)
        return JsonResponse({'results':results})

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


# returns a dictionary with all objects saved.
def data_validations_and_save(**kwargs):
    objects_saved = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            objects_saved[key_form] = form.save()
        else:
            return JsonResponse({'error':f'Check {key_form}'})
    return objects_saved

def calculate(data):

    data = SimpleNamespace(**data)

    working_area = [data.size_x-data.offset_left-data.offset_right,data.size_y-data.offset_top-data.offset_bottom]

    if data.main_property==1:
        n_bands = int(data.value)
        number_of_gaps = n_bands - 1
        sum_gaps_size = data.gap*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
    else:
        length = data.value
        n_bands = int(math.trunc(working_area[0]/(length+data.gap)))

    volEstimate = returnDropEstimateVol(data)
    list_of_bands = []
    
    deltaX = float(data.delta_x)
    deltaY = float(data.delta_y)
    for i in range(0,n_bands):
        bandlist = []
        zeros=(i*(length+data.gap))+data.offset_left
        for j in range(volEstimate[i][2]):
            if j % 2:
                current_height = deltaY/2
                while current_height <= data.height:
                    applicationline=[]
                    current_length=deltaX/2
                    while current_length<=length:
                        applicationline.append([float(data.offset_bottom)+current_height, current_length+float(zeros)])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline=[]
                    current_length=0.
                    while current_length<=length:
                        applicationline.append([float(data.offset_bottom)+current_height, current_length+float(zeros)])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
        list_of_bands.append(bandlist)

    # Creates the Gcode for the application and return it
    return gcode_generation(list_of_bands, data.motor_speed, data.frequency, data.temperature, data.pressure, [data.zero_x,data.zero_y])


def gcode_generation(list_of_bands, speed, frequency, temperature, pressure, zeroPosition):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)
        generate.hold_bed_temperature(temperature)
        generate.report_bed_temperature(4)

    # Move to the home
    # generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)

    # Application
    # generate.pressurize(pressure)
    list_of_bands = list_of_bands[::-1]
    for band in list_of_bands:
        generate.rinsing()
        generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
        jj = 0
        for index, list_of_points in enumerate(band):
            list_of_points = list_of_points[::-1]
            for point in list_of_points:
                generate.linear_move_xy(point[1], point[0], speed)
                generate.finish_moves()
                generate.pressurize(pressure)
                generate.open_valve(frequency)
                generate.finish_moves()
                jj += 1
                if jj > 50:
                    generate.rinsing()
                    generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
                    jj = 0
    #Stop heating
    if (temperature !=0):
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    #Homming
    generate.homming("XY")
    return generate.list_of_gcodes


