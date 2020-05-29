from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SampleApplication_Form, PlateProperties_Form, BandSettings_Form, MovementSettings_Form, PressureSettings_Form
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db, MovementSettings_Db, PressureSettings_Db, SampleApplication_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
# Create your views here.
from printrun import printcore, gcoder

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
            x = float(request.POST.get('x'))
            y = float(request.POST.get('y'))

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
        # Treatment for play button
        if 'START' in request.POST:
            sample_application_form  =   SampleApplication_Form(request.POST)
            plate_properties_form    =   PlateProperties_Form(request.POST)
            band_settings_form       =   BandSettings_Form(request.POST)
            movement_settings_form   =   MovementSettings_Form(request.POST)
            pressure_settings_form   =   PressureSettings_Form(request.POST)
            # f = SampleAppForm(request.POST)
            # if f.is_valid():
            if sample_application_form.is_valid():
                file_name = sample_application_form.cleaned_data['file_name']
            else:
                print('sample_application_form')

            if plate_properties_form.is_valid():
                size_x = int(plate_properties_form.cleaned_data['size_x'])
                size_y = int(plate_properties_form.cleaned_data['size_y'])
                offset_x = int(plate_properties_form.cleaned_data['offset_x'])
                offset_y = int(plate_properties_form.cleaned_data['offset_y'])
            else:
                print('plate_properties_form')

            if band_settings_form.is_valid():
                main_property = int(band_settings_form.cleaned_data['main_property'])
                value = int(band_settings_form.cleaned_data['value'])
                height = int(band_settings_form.cleaned_data['height'])
                gap = int(band_settings_form.cleaned_data['gap'])
            else:
                print('band_settings_form')

            if movement_settings_form.is_valid():
                motor_speed = int(movement_settings_form.cleaned_data['motor_speed'])
                delta_x = int(movement_settings_form.cleaned_data['delta_x'])
                delta_y = int(movement_settings_form.cleaned_data['delta_y'])
            else:
                print('movement_settings_form')

            if pressure_settings_form.is_valid():
                pressure = int(pressure_settings_form.cleaned_data['pressure'])
                delta_pressure = int(pressure_settings_form.cleaned_data['delta_pressure'])
            else:
                print('pressure_settings_form')


            working_area = [size_x-2*offset_x,size_y-2*offset_y]


            if main_property==1:
                n_bands = value
                number_of_gaps = n_bands - 1;
                sum_gaps_size = gap*number_of_gaps;
                length = (working_area[0]-sum_gaps_size)/n_bands
            else:
                length = value
                n_bands = math.trunc(working_area[0]/(length+gap))

            applicationsurface = []
            current_height = 0
            while current_height <= height:
                for i in range(0,n_bands):
                    applicationline=[]
                    current_length=0
                    zeros=(i*(length+gap))+offset_x
                    while current_length<=length:
                        applicationline.append([offset_y+current_height, current_length+zeros])
                        current_length+=delta_x
                    applicationsurface.append(applicationline)
                current_height+=delta_y
            frequency = delta_pressure

            # Creates the Gcode for the app
            gcode = GcodeGen(applicationsurface, motor_speed, frequency)

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
            OC_LAB.send_now('M84')
            return JsonResponse({'message':'stopped'})
        if 'PAUSE' in request.POST:
            print(request.POST)
            return JsonResponse({'message':'paused'})

class SampleAppSaveAndLoad(View):
    def post(self, request):
        sample_application_form  =   SampleApplication_Form(request.POST, request.user)
        plate_properties_form    =   PlateProperties_Form(request.POST)
        band_settings_form       =   BandSettings_Form(request.POST)
        movement_settings_form   =   MovementSettings_Form(request.POST)
        pressure_settings_form   =   PressureSettings_Form(request.POST)


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
                sample_application_object = sample_application_form.save(commit=False)
                sample_application_object.auth = request.user
                sample_application_object.movement_settings = movement_settings_object
                sample_application_object.pressure_settings = pressure_settings_object
                sample_application_object.plate_properties = plate_properties_object
                sample_application_object.band_settings = band_settings_object
                print(pressure_settings_object)
                sample_application_object.save()
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
        #
        sample_application_conf.update(plate_properties_conf)
        sample_application_conf.update(band_settings_conf)
        sample_application_conf.update(movement_settings_conf)
        sample_application_conf.update(pressure_settings_conf)

        # print(sample_application_conf)
        return JsonResponse(sample_application_conf)

def GcodeGen(listoflines, speed, frequency):
    gcode=['G94 P400']
    for listofpoints in listoflines:
        for point in listofpoints:
            gline = 'G1Y{}X{}F{}'.format(str(point[0]), str(point[1]), speed)
            gcode.append(gline)
            gcode.append('M400')
            gcode.append(f'G93 F{frequency} P400')
            gcode.append('M400')
        # gcode.append('G94 P300')
            # gcode += 'M42 P13 S255 \n'
        # gcode = gcode[:gcode.rfind('M42 P13 S255 \n')]
        # gcode += 'M42 P13 S0 \n' # End of line
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
