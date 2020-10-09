from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

import json
import numpy as np
import math
from scipy.optimize import minimize
from printrun import printcore, gcoder
from types import SimpleNamespace

from .forms import *
from .models import *
from .flowCalc import FlowCalc

from finecontrol.forms import ZeroPosition_Form
from finecontrol.models import ZeroPosition
from connection.forms import OC_LAB

forms = {
    'SampleApplication_Form': SampleApplication_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'BandSettings_Form': BandSettings_Form(),
    'MovementSettings_Form': MovementSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    'BandComponents_Form':BandsComponents_Form(),
    'ZeroPosition_Form': ZeroPosition_Form()
    }

class Sample(FormView):
    def get(self, request):
        # Load the list with all the saved data
        if 'LISTLOAD' in request.GET:
            sample_application = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
            data_saved = [[i.file_name,i.id] for i in sample_application]
            return JsonResponse(data_saved, safe=False)
        else:
            forms['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
            return render(request,'sample.html',forms)


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
                light_gcode = gcoder.LightGCode(gcode)
                OC_LAB.startprint(light_gcode)
                return JsonResponse({'error':'f.errors'})

        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message':'stopped'})

        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message':'paused'})

class SampleAppSaveAndLoad(View):
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

        table_data = json.loads(request.POST.get('table'))

        # If everything is OK then it checks the name and tries to save the Complete Sample App
        if sample_application_form.is_valid():
            filename = sample_application_form.cleaned_data['file_name']
            in_db=SampleApplication_Db.objects.filter(file_name=filename).filter(auth_id=request.user)
            # Check if theres
            if len(in_db)>0:
                return JsonResponse({'error':'File Name already exists!'})
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
                        bands_components_instance
                    else:
                        JsonResponse({'error':bands_components_form.errors})
          
                return JsonResponse({'message':f'The File {filename} was saved!'})

        else:
            return JsonResponse({'error':'Please fill in the filename!'})

    def get(self, request):
        file_name=request.GET.get('filename')
        print(file_name)
        sample_application_conf=model_to_dict(SampleApplication_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Db.objects.get(id=sample_application_conf['plate_properties']))
        band_settings_conf=model_to_dict(BandSettings_Db.objects.get(id=sample_application_conf['band_settings']))
        movement_settings_conf=model_to_dict(MovementSettings_Db.objects.get(id=sample_application_conf['movement_settings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Db.objects.get(id=sample_application_conf['pressure_settings']))
        zero_position_conf=model_to_dict(ZeroPosition.objects.get(id=sample_application_conf['zero_position']))
        bands_components = BandsComponents_Db.objects.filter(sample_application=SampleApplication_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])

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
        # print(sample_application_conf)
        return JsonResponse(sample_application_conf)

class CalcVol(View):
    def post(self, request):
        data = SimpleNamespace(**request.POST)
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


def calculateDeltaX(length,height,maxPoints):
    '''calculates the distance of the points if deltaX == deltaY'''

    #deltaX = [0,0]
    deltaX = - ((length+height)/(2*(1-maxPoints))) + math.sqrt(((length+height)/(2*(1-maxPoints)))**2-((length*height)/(1-maxPoints)))
    #deltaX[1] = - ((length+height)/(2*(1-maxPoints))) - math.sqrt(((length+height)/(2*(1-maxPoints)))**2-((length*height)/(1-maxPoints)))

    return deltaX

def optimizeMaxPoints(length, height, maxPoints):
    '''calculates the error function, so it can
    be minimized to get the best number of points'''

    deltaX = calculateDeltaX(length,height,maxPoints)
    pointsX = np.round(length / deltaX)
    pointsY = np.round(height / deltaX)

    error = (pointsX * deltaX - length)**2 + (pointsY * deltaX - height)**2

    return error

def minimizeDeltaX(length, height, volume, bandNum, data):
    '''calculates deltaX according to the set volume'''
    #print(data)
    dropVolume = FlowCalc(pressure=float(data.pressure), nozzleDiameter=data.nozzlediameter, frequency = float(data.frequency), fluid=data.table[bandNum]['type'], density=data.table[bandNum]['density'], viscosity=data.table[bandNum]['viscosity']).calcVolume()
    print("dropVolume: "+str(dropVolume))
    #dropVolume = 0.025

    optimizeTest = lambda maxPoints: optimizeMaxPoints(length, height, maxPoints)
    x0 = volume / dropVolume
    res = minimize(optimizeTest,x0)
    points = np.round(res.x)
    deltaX = calculateDeltaX(length,height,points)
    realVolume = points * dropVolume

    return [deltaX[0], realVolume]

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

    applicationsurface = []
    for i in range(0,n_bands):
        if data.table[i]['volume (ul)'] == "null" or data.table[i]['volume (ul)'] == "":
            deltaX = float(data.delta_x)
            deltaY = float(data.delta_y)
        else:
            [deltaX, realVolume] = minimizeDeltaX(float(length), float(data.height), float(data.table[i]['volume (ul)']), i, data)
            if deltaX < 0.0002:
                deltaX = 0.0002
            deltaY = deltaX


        print("deltaX: "+str(deltaX))

        zeros=(i*(length+data.gap))+data.offset_left
        current_height = 0.
        while current_height <= data.height:
            applicationline=[]
            current_length=0.
            while current_length<=length:
                applicationline.append([float(data.offset_bottom)+current_height, current_length+float(zeros)])
                current_length+=deltaX
            applicationsurface.append(applicationline)
            current_height+=deltaY

    # Creates the Gcode for the application and return it
    return GcodeGen(applicationsurface, data.motor_speed, data.frequency, data.temperature, data.pressure, [data.zero_x,data.zero_y])

def GcodeGen(listoflines, speed, frequency, temperature, pressure, zeroPosition):
    gcode=list()
    # No HEATBED CASE
    if temperature!=0:
        gcode=[f'M190 R{temperature}']
    # Move to the home
    gcode.append('G28XY')
    gline = 'G1Y{}X{}F{}'.format(str(round(zeroPosition[1],3)), str(round(zeroPosition[0],3)), speed)
    gcode.append(gline)
    gcode.append('G92X0Y0')
    gcode.append('M400')
    # Only MOVEMENT CASE
    if pressure==0 and frequency==0:
        gcode.append(f'G94 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(round(point[0],3)), str(round(point[1],3)), speed)
                gcode.append(gline)
                gcode.append('M400')

    # Normal Application
    else:
        gcode.append(f'G97 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(round(point[0],3)), str(round(point[1],3)), speed)
                gcode.append(gline)
                gcode.append('M400')
                gcode.append(f'G97 P{pressure}')
                gcode.append(f'G98 F{frequency}')
                gcode.append('M400')
    gcode.append('G28XY')
    return gcode

def returnDropEstimateVol(data):

    working_area = [float(data.size_x[0])-float(data.offset_left[0])-float(data.offset_right[0]),float(data.size_y[0])-float(data.offset_top[0])-float(data.offset_bottom[0])]
    if data.main_property[0]==1:
        n_bands = int(data.value[0])
        number_of_gaps = n_bands - 1
        sum_gaps_size = data.gap[0]*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
    else:
        length = data.value[0]
        n_bands = int(math.trunc(working_area[0]/(float(length)+float(data.gap[0]))))


    dataTable = json.loads(data.table[0])
    results = []
    for table in dataTable:

        dropVolume = FlowCalc(pressure=float(data.pressure[0]), nozzleDiameter=data.nozzlediameter[0], frequency = float(data.frequency[0]), fluid=table['type'], density=table['density'], viscosity=table['viscosity']).calcVolume()


        if table['volume (ul)'] == "" or table['volume (ul)'] == "null":
            pointsX = np.round(float(length)/float(data.delta_x[0]))
            pointsY = 1
            if data.height[0] != "0":
                pointsY = np.round(float(data.height[0])/float(data.delta_y[0]))
            realVolume = pointsX * pointsY * dropVolume

        else:
            optimizeTest = lambda maxPoints: optimizeMaxPoints(float(length), float(data.height[0]), maxPoints)
            x0 = float(table['volume (ul)']) / dropVolume
            res = minimize(optimizeTest,x0)
            points = np.round(res.x)
            realVolume = points[0] * dropVolume


        #np.append(results, [dropVolume, realVolume])
        results.append([dropVolume, realVolume])

    return results