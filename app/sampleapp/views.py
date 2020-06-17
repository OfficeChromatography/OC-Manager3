from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SampleApplication_Form, PlateProperties_Form, BandSettings_Form, MovementSettings_Form, PressureSettings_Form, BandsComponents_Form
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db, MovementSettings_Db, PressureSettings_Db, SampleApplication_Db, BandsComponents_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
# Create your views here.
from printrun import printcore, gcoder
import json
from decimal import *

forms = {
    'SampleApplication_Form': SampleApplication_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'BandSettings_Form': BandSettings_Form(),
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
            gcode = f'G28\nG0X{x_mov}Y{y_mov}\nG92X0Y0'
            OC_LAB.send(gcode)
            return JsonResponse({'message':'ok'})
        except ValueError:
            return JsonResponse({'error':'Error check values'})




class Sample(FormView):
    def get(self, request):
        # Send the saved config files
        forms['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
        return render(request,'sample.html',forms)

class SampleAppPlay(View):
    def post(self, request):
        print(request.POST)
        # Treatment for play button
        if 'START' in request.POST:
            if OC_LAB.paused == True:
                OC_LAB.resume()
            else:
                plate_properties_form    =   PlateProperties_Form(request.POST)
                band_settings_form       =   BandSettings_Form(request.POST)
                movement_settings_form   =   MovementSettings_Form(request.POST)
                pressure_settings_form   =   PressureSettings_Form(request.POST)


                if plate_properties_form.is_valid():
                    size_x = Decimal(plate_properties_form.cleaned_data['size_x'])
                    size_y = Decimal(plate_properties_form.cleaned_data['size_y'])
                    offset_right = Decimal(plate_properties_form.cleaned_data['offset_right'])
                    offset_left = Decimal(plate_properties_form.cleaned_data['offset_left'])
                    offset_top = Decimal(plate_properties_form.cleaned_data['offset_top'])
                    offset_bottom = Decimal(plate_properties_form.cleaned_data['offset_bottom'])

                else:
                    print('plate_properties_form')

                if band_settings_form.is_valid():
                    main_property = int(band_settings_form.cleaned_data['main_property'])
                    value = Decimal(band_settings_form.cleaned_data['value'])
                    height = Decimal(band_settings_form.cleaned_data['height'])
                    gap = Decimal(band_settings_form.cleaned_data['gap'])
                else:
                    print('band_settings_form')

                if movement_settings_form.is_valid():
                    motor_speed = int(movement_settings_form.cleaned_data['motor_speed'])
                    delta_x = Decimal(movement_settings_form.cleaned_data['delta_x'])
                    delta_y = Decimal(movement_settings_form.cleaned_data['delta_y'])
                    print(delta_x)
                else:
                    print('movement_settings_form')

                if pressure_settings_form.is_valid():
                    pressure = Decimal(pressure_settings_form.cleaned_data['pressure'])
                    frequency = Decimal(pressure_settings_form.cleaned_data['frequency'])
                    try:
                        temperature = Decimal(pressure_settings_form.cleaned_data['temperature'])
                    except TypeError:
                        temperature = 0
                else:
                    print('pressure_settings_form')


                working_area = [size_x-offset_left-offset_right,size_y-offset_top-offset_bottom]


                if main_property==1:
                    n_bands = int(value)
                    number_of_gaps = n_bands - 1;
                    sum_gaps_size = gap*number_of_gaps;
                    length = (working_area[0]-sum_gaps_size)/n_bands
                else:
                    length = value
                    n_bands = int(math.trunc(working_area[0]/(length+gap)))

                applicationsurface = []
                current_height = 0
                while current_height <= height:
                    for i in range(0,n_bands):
                        applicationline=[]
                        current_length=0
                        zeros=(i*(length+gap))+offset_left
                        while current_length<=length:
                            applicationline.append([offset_bottom+current_height, current_length+zeros])
                            current_length+=delta_x
                        applicationsurface.append(applicationline)
                    current_height+=delta_y

                # Creates the Gcode for the app
                gcode = GcodeGen(applicationsurface, motor_speed, frequency, temperature, pressure)

                # Save it in a file
                f = open("file.gcode", "w+")
                for i in gcode:
                    f.write(i+'\n')
                f.close()

                # Open from the file and startprint
                gcode1 = [code_line.strip() for code_line in open("file.gcode")]
                light_gcode = gcoder.LightGCode(gcode1)
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
        print(request.POST)
        sample_application_form  =   SampleApplication_Form(request.POST, request.user)
        plate_properties_form    =   PlateProperties_Form(request.POST)
        band_settings_form       =   BandSettings_Form(request.POST)
        movement_settings_form   =   MovementSettings_Form(request.POST)
        pressure_settings_form   =   PressureSettings_Form(request.POST)

        table = request.POST.get('table')
        table_data = json.loads(table)

        # Check Plate Property Formular
        if plate_properties_form.is_valid():
            plate_properties_object = plate_properties_form.save()
        else:
            return JsonResponse({'error':'Check plate properties'})

        # Check Band Settings Formular
        if band_settings_form.is_valid():
            band_settings_object = band_settings_form.save()
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
        if sample_application_form.is_valid():
            filename = sample_application_form.cleaned_data['file_name']
            in_db=SampleApplication_Db.objects.filter(file_name=filename).filter(auth_id=request.user)

            # Check if theres
            if len(in_db)>0:
                return JsonResponse({'error':'File Name exist!'})
            else:
                sample_application_instance = sample_application_form.save(commit=False)
                sample_application_instance.auth = request.user
                sample_application_instance.movement_settings = movement_settings_object
                sample_application_instance.pressure_settings = pressure_settings_object
                sample_application_instance.plate_properties = plate_properties_object
                sample_application_instance.band_settings = band_settings_object
                new_sample_application=sample_application_instance.save()


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
            return JsonResponse({'error':'Please fill the filename!'})

    def get(self, request):
        file_name=request.GET.get('filename')

        # print(file_name)
        sample_application_conf=model_to_dict(SampleApplication_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Db.objects.get(id=sample_application_conf['plate_properties']))
        band_settings_conf=model_to_dict(BandSettings_Db.objects.get(id=sample_application_conf['band_settings']))
        movement_settings_conf=model_to_dict(MovementSettings_Db.objects.get(id=sample_application_conf['movement_settings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Db.objects.get(id=sample_application_conf['pressure_settings']))

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
        # print(sample_application_conf)
        return JsonResponse(sample_application_conf)


# AUX Functions

def GcodeGen(listoflines, speed, frequency, temperature, pressure):
    gcode=list()

    # No HEATBED CASE
    if temperature!=0:
        gcode=[f'M190 R{temperature}']

    # Only MOVEMENT CASE
    if pressure==0 and frequency==0:
        gcode.append(f'G94 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(point[0]), str(point[1]), speed)
                gcode.append(gline)
                gcode.append('M400')

    # Normal Application
    else:
        gcode.append(f'G94 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(point[0]), str(point[1]), speed)
                gcode.append(gline)
                gcode.append('M400')
                gcode.append(f'G93 F{frequency} P{pressure}')
                gcode.append('M400')



    gcode.append('G28')
    return gcode

def dinamic_cleaning():
    # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
    # range(start, stop, step)
    time = 5 # Minimun time for each frequency 5 sec
    f = open("dinamic_clean.gcode", "w+")
    for i in range(100,550,50):
        for j in range(1,5*i+1):
            f.write(f'G93 F{i} P300'+'\n')
    f.close()

def static_cleaning():
    # THE GCODE TO PUMP NO MATTER THE PRESSURE
    gcode = ''
    # OPEN DE VALVE AND LEAVE IT LIKE THAT
    f = open("static_clean.gcode", "w+")
    for i in range(0,100):
        f.write(gcode+f'{i}'+'\n')
    f.close()
