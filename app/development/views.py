from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import Development_Form, PlateProperties_Form, DevelopmentBandSettings_Form, MovementSettings_Form, PressureSettings_Form
from .models import Development_Db, BandSettings_Dev_Db, PlateProperties_Dev_Db, MovementSettings_Dev_Db, PressureSettings_Dev_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
from printrun import printcore, gcoder
from types import SimpleNamespace
import json
from decimal import *
from .flowCalc import FlowCalc

forms = {
    'Development_Form': Development_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'DevelopmentBandSettings_Form': DevelopmentBandSettings_Form(),
    'MovementSettings_Form': MovementSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    }

class HommingSetup(View):
    def post(self, request):
        try:
            x = Decimal(request.POST.get('x'))
            y = Decimal(request.POST.get('y'))
            # Calculate the movement
            x_mov = 50-(x/2)
            y_mov = 30+((100-y)/2)
            gcode = f'G28XY\nG0X{x_mov}Y{y_mov}\nG92X0Y0'
            OC_LAB.send(gcode)
            return JsonResponse({'message':'ok'})
        except ValueError:
            return JsonResponse({'error':'Error check values'})

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
                                    movement_settings_form   =   MovementSettings_Form(request.POST),
                                    pressure_settings_form   =   PressureSettings_Form(request.POST))

                
                
                devBandSettings = request.POST.get('devBandSettings')
                devBandSettings_data = json.loads(devBandSettings)
                developmentBandSettings_form = DevelopmentBandSettings_Form(devBandSettings_data)
                if developmentBandSettings_form.is_valid():
                    forms_data.update(devBandSettings_data)
                else:
                    return JsonResponse({'error':'Check band properties'})
                
                # With the data, gcode is generated
                gcode = calculateDevelopment(forms_data)
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

class DevelopmentSaveAndLoad(View):
    def post(self, request):
        #print(request.POST)
        development_form  =   Development_Form(request.POST, request.user)
        plate_properties_form    =   PlateProperties_Form(request.POST)
        #developmentBandSettings_form       =   DevelopmentBandSettings_Form(request.POST)
        movement_settings_form   =   MovementSettings_Form(request.POST)
        pressure_settings_form   =   PressureSettings_Form(request.POST)

        devBandSettings = request.POST.get('devBandSettings')
        devBandSettings_data = json.loads(devBandSettings)

        # Check Plate Property Formular
        if plate_properties_form.is_valid():
            plate_properties_object = plate_properties_form.save()
        else:
            return JsonResponse({'error':'Check plate properties'})

        # Check Band Settings Formular
        developmentBandSettings_form = DevelopmentBandSettings_Form(devBandSettings_data)
        if developmentBandSettings_form.is_valid():
            print('hello')
            developmentBandSettings_object = developmentBandSettings_form.save()
        else:
            return JsonResponse({'error':'Check band properties'})

        # Check Movement Settings Formular
        if movement_settings_form.is_valid():
            movement_settings_object = movement_settings_form.save()
        else:
            return JsonResponse({'error':'Check movement settings'})

        # Check Pressure Settings Formular
        if pressure_settings_form.is_valid():
            pressure_settings_object = pressure_settings_form.save()
        else:
            return JsonResponse({'error':'Check pressure settings'})


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
                development_instance.movement_settings = movement_settings_object
                development_instance.pressure_settings = pressure_settings_object
                development_instance.plate_properties = plate_properties_object
                development_instance.developmentBandSettings = developmentBandSettings_object
                new_development=development_instance.save()

                return JsonResponse({'message':f'The File {filename} was saved!'})

        else:
            return JsonResponse({'error':'Please fill the filename!'})

    def get(self, request):
        file_name=request.GET.get('filename')

        
        development_conf=model_to_dict(Development_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Dev_Db.objects.get(id=development_conf['plate_properties']))
        developmentBandSettings_conf=model_to_dict(BandSettings_Dev_Db.objects.get(id=development_conf['developmentBandSettings']))
        movement_settings_conf=model_to_dict(MovementSettings_Dev_Db.objects.get(id=development_conf['movement_settings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Dev_Db.objects.get(id=development_conf['pressure_settings']))

        development_conf.update(plate_properties_conf)
        development_conf.update(developmentBandSettings_conf)
        development_conf.update(movement_settings_conf)
        development_conf.update(pressure_settings_conf)
        
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

def calculateDevelopment(data):
    #dropvolume in uL
    dropVolume = FlowCalc(pressure=float(data['pressure']), nozzleDiameter=data['nozzlediameter'], frequency = float(data['frequency']), fluid=data['fluid'], density=data['density'], viscosity=data['viscosity']).calcVolume()
    print("dropVolume: "+str(dropVolume))
    #dropVolume = 0.025
    data = SimpleNamespace(**data)
    
    length = float(data.size_x)-float(data.offset_left)-float(data.offset_right)

    points = round(float(data.volume) / dropVolume)
    pointsPerLine = round(length / float(data.delta_x))
    lines = round(points / pointsPerLine)
    #realVolume = lines * pointsPerLine * dropVolume

    applicationLine=[]
    current_length=0
    while current_length<=length:
        applicationLine.append([round(float(data.offset_bottom),3), round(float(data.offset_left)+current_length,3)])
        current_length+=float(data.delta_x)

    applicationLines=[]
    line = 0
    if (data.printBothways=='On'):
        while line < lines:
            if (line == 0) or (line%2 == 0):
                applicationLines.extend(applicationLine)
            else:
                applicationLines.extend(applicationLine[::-1])
            line+=1
    else:
        while line < lines:
            applicationLines.extend(applicationLine)
            line+=1
    
    # Creates the Gcode for the application and return it
    #print(applicationLines)
    return GcodeGenDevelopment(applicationLines, data.motor_speed, data.frequency, data.temperature, data.pressure)


def GcodeGenDevelopment(line, speed, frequency, temperature, pressure):
    gcode=list()
    # No HEATBED CASE
    if temperature!=0:
        gcode=[f'M190 R{temperature}']
    
    gcode.append('G28XY')
    glineY = 'G1Y{}F{}'.format(str(point[0]+19.2), speed)
    gcode.append(glineY)
    gcode.append(f'G97 P{pressure}')
    for point in line:
        glineX = 'G1X{}F{}'.format(str(point[1]+7), speed)
        gcode.append(glineX)
        gcode.append('M400')
        gcode.append(f'G97 P{pressure}')
        gcode.append(f'G98 F{frequency}')
        gcode.append('M400')
    gcode.append('G28XY')
    return gcode

class DevelopmentCalc(View):
    def post(self, request):
        data = SimpleNamespace(**request.POST)
        results = returnDropEstimateVol(data)
        return JsonResponse({'results':results})

def returnDropEstimateVol(data):
    table = json.loads(data.devBandSettings[0])
    
    dropVolume = FlowCalc(pressure=float(data.pressure[0]), nozzleDiameter=data.nozzlediameter[0], frequency = float(data.frequency[0]), fluid=table['fluid'], density=table['density'], viscosity=table['viscosity']).calcVolume()
        
    length = float(data.size_x[0])-float(data.offset_left[0])-float(data.offset_right[0])
    points = round(float(data.volume[0]) / dropVolume)
    pointsPerLine = round(length / float(data.delta_x[0]))
    lines = round(points / pointsPerLine)
    realVolume = lines * pointsPerLine * dropVolume

    return [dropVolume, realVolume]