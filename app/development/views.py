from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import Development_Form, PlateProperties_Form, DevelopmentBandSettings_Form, PressureSettings_Form
from .models import Development_Db, BandSettings_Dev_Db, PlateProperties_Dev_Db, PressureSettings_Dev_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
from printrun import printcore, gcoder
from types import SimpleNamespace
import json
from decimal import *
from .flowCalc import FlowCalc
from finecontrol.forms import ZeroPosition_Form
from finecontrol.models import ZeroPosition

forms = {
    'Development_Form': Development_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'DevelopmentBandSettings_Form': DevelopmentBandSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    'ZeroPosition_Form': ZeroPosition_Form()
    }

# class HommingSetup(View):
#     def post(self, request):
#         try:
#             x = Decimal(request.POST.get('x'))
#             y = Decimal(request.POST.get('y'))
#             # Calculate the movement
#             x_mov = 50-(x/2)
#             y_mov = 30+((100-y)/2)
#             gcode = f'G28XY\nG0X{x_mov}Y{y_mov}\nG92X0Y0'
#             OC_LAB.send(gcode)
#             return JsonResponse({'message':'ok'})
#         except ValueError:
#             return JsonResponse({'error':'Error check values'})

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
        pressure_settings_form = PressureSettings_Form(request.POST)
        #developmentBandSettings_form       =   DevelopmentBandSettings_Form(request.POST)
        zero_position_form       =   ZeroPosition_Form(request.POST)

        devBandSettings = request.POST.get('devBandSettings')
        devBandSettings_data = json.loads(devBandSettings)
        #print(devBandSettings_data)
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

        development_conf.update(plate_properties_conf)
        development_conf.update(developmentBandSettings_conf)
        development_conf.update(pressure_settings_conf)
        development_conf.update(zero_position_conf)
        
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
    # #flow in uL/s
    volume = FlowCalc(pressure=float(data['pressure']), nozzleDiameter=data['nozzlediameter'], fluid=data['fluid'], density=data['density'], viscosity=data['viscosity']).calcFlow()
    # #syringe movement in mm/s
    flow = flow / 58
    # #maximum speed in mm/min
    speed = flow * 60
    

    data = SimpleNamespace(**data)
    #print(data)
    
    length = float(data.size_x)-float(data.offset_left)-float(data.offset_right)
    startPoint = [round(float(data.offset_left)+float(data.zero_x),3), round(float(data.offset_bottom)+float(data.zero_y),3)]
    
    zMovement = round(float(data.volume) * 60/1000,3)
    #time in seconds
    time = zMovement / speed * 60

    #add error for when time is greater than 3

    return GcodeGenDevelopment(startPoint, length, zMovement, data.applications, data.printBothways, speed, data.temperature, data.precision, data.pressure)


def GcodeGenDevelopment(startPoint, length, zMovement, applications, printBothways, speed, temperature, precision, pressure):
    gcode=list()

    # No HEATBED CASE
    if temperature!=0:
        gcode=[f'M190 R{temperature}']
    
    gcode.append('G28XY')
    glineY = f'G1Y{startPoint[1]}F{speed}'
    gcode.append(glineY)
    
    glineX = f'G1X{startPoint[0]}F{speed}'
    gcode.append(glineX)
    gcode.append('M400')

    gcode.append('G91')
    jj = 0   
    for x in range(int(applications)*2):
        if (x%2)==0:
            for yy in range(int(precision)):
                gcode.append(f'G97 P{pressure}')
                gcode.append('G40')
                glineX = f'G1X{length/float(precision)}Z{zMovement/float(applications)/float(precision)}F{speed}'
                gcode.append(glineX)
                gcode.append('G40')
            jj += 1
        else:
            if printBothways == 'On':
                for yy in range(int(precision)):
                    gcode.append(f'G97 P{pressure}')
                    gcode.append('G40')
                    glineX = f'G1X-{length/float(precision)}Z{zMovement/float(applications)/float(precision)}F{speed}'
                    gcode.append(glineX)
                    gcode.append('G40')
                jj += 1
            else:
                glineX = f'G1X-{length}F{speed}'
                gcode.append(glineX)
        if jj >= int(applications):
            break     
    gcode.append('G90')
    gcode.append('G28XY')
    return gcode

# class DevelopmentCalc(View):
#     def post(self, request):
#         data = SimpleNamespace(**request.POST)
#         results = returnFlow(data)
#         return JsonResponse({'results':results})

# def returnFlow(data):
#     table = json.loads(data.devBandSettings[0])
    
#     flow = FlowCalc(pressure=float(data.pressure[0]), nozzleDiameter=data.nozzlediameter[0], fluid=table['fluid'], density=table['density'], viscosity=table['viscosity']).calcFlow()
        

#     return flow