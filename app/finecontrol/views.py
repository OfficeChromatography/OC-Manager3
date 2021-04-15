from connection.forms import OC_LAB
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .forms import *
from .models import *
import os
from finecontrol.calculations.volumeToZMovement import volumeToZMovement
from finecontrol.gcode.GcodeGenerator import GcodeGenerator

from django.views.generic import FormView, View
from django.http import JsonResponse

from sampleapp.models import SampleApplication_Db, BandsComponents_Db
from development.models import Development_Db
from derivatization.models import Derivatization_Db
from detection.models import Images_Db

from django.forms.models import model_to_dict


CLEANINGPROCESS_INITIALS = {'start_frequency':100,
                            'stop_frequency':500,
                            'steps':50,
                            'pressure':20}
form ={}


class MethodList(View):

    def get(self, request):
        """Returns a list with all the Methods saved in DB"""
        method = Method_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = []
        for i in method:
            icons = [1,1,1,1]
            if not SampleApplication_Db.objects.filter(method=i):
                icons[0] = 0.3
            if not Development_Db.objects.filter(method=i):
                icons[1] = 0.3
            if not Derivatization_Db.objects.filter(method=i):
                icons[2] = 0.3
            if not Images_Db.objects.filter(method=i):
                icons[3] = 0.3
            data_saved.append([i.filename,i.id,icons])
        return JsonResponse(data_saved, safe=False)

class Export(View):
    def get(self, request, id):
        response={}
        method = Method_Db.objects.get(pk=id)
        if SampleApplication_Db.objects.filter(method=method):
            sample_config = SampleApplication_Db.objects.get(method=method)
            response.update(model_to_dict(sample_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.band_settings.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.zero_properties.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.movement_settings.get(), exclude=["id",]))
            bands_components = BandsComponents_Db.objects.filter(sample_application=sample_config.id).values()
            response.update({'bands_components': [entry for entry in bands_components]})
        if Development_Db.objects.filter(method=method):
            dev_config = Development_Db.objects.get(method=method)
            response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id",]))
            response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id",]))
            flowrate_entry = Flowrate_Db.objects.filter(development=dev_config.id).values('value')
            response.update({'flowrate': [entry for entry in flowrate_entry]})
        if Derivatization_Db.objects.filter(method=method):
            der_config = Derivatization_Db.objects.get(method=method)
            response.update(model_to_dict(der_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(der_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(der_config.band_settings.get(), exclude=["id",]))
            response.update(model_to_dict(der_config.zero_properties.get(), exclude=["id",]))
        if Images_Db.objects.filter(method=method):
            images = Images_Db.objects.filter(method=method)
            for imageconf in images:
                user_conf = model_to_dict(imageconf.user_conf,
                                    fields=[field.name for field in imageconf.user_conf._meta.fields])
                leds_conf = model_to_dict(imageconf.leds_conf,
                                        fields=[field.name for field in imageconf.leds_conf._meta.fields])
                camera_conf = model_to_dict(imageconf.camera_conf,
                                        fields=[field.name for field in imageconf.camera_conf._meta.fields])
                response.update({**{
                        'url': imageconf.image.url,
                        'user_conf': user_conf,
                        'leds_conf': leds_conf,
                        'camera_conf': camera_conf,
                        'note': imageconf.note,
                        }})

        return JsonResponse(response)


class OcLabControl(View):
    def post(self,request):
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message':'OcLab Paused!'})
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message':'OcLab Stopped!'})
        if 'RESUME' in request.POST:
            OC_LAB.resume()
            return JsonResponse({'message':'OcLab Resumed!'})
        if 'SEND' in request.POST:
            OC_LAB.send(request.POST['message'])
            return JsonResponse({'message':f'OcLab {request.POST["message"]} send !'})
        if 'SEND_NOW' in request.POST:
            OC_LAB.send_now(request.POST['message'])
            return JsonResponse({'message':f'OcLab {request.POST["message"]} fast send !'})
        if 'RESET' in request.POST:
            OC_LAB.reset()
            return JsonResponse({'message':f'OcLab {request.POST["message"]} reset !'})

class SyringeLoad(View):
    # def post:
    def get(self, request):
        if "LISTLOAD" in request.GET:
            syringe_load_db = SyringeLoad_Db.objects.filter(author=request.user).order_by('volume')
            volumes = [i.volume for i in syringe_load_db]
            return JsonResponse(volumes, safe=False)

    def post(self, request):
        # Creates a new vol in the database
        if 'SAVEMOVEMOTOR' in request.POST:
            try:
                SyringeLoad_Db.objects.filter(volume=request.POST['SAVEMOVEMOTOR']).filter(author=request.user)[0]
                return JsonResponse("Volume already exist!", safe=False)
            except IndexError:
                syringe_load = SyringeLoad_Db.objects.create(volume=request.POST['SAVEMOVEMOTOR'],
                                                             author=request.user)
                syringe_load.save()
                return JsonResponse("Volume saved!", safe=False)

        if 'DELETE' in request.POST:
            try:
                SyringeLoad_Db.objects.filter(volume=request.POST['DELETE']).filter(author=request.user)[0].delete()
                return JsonResponse("Volume Deleted!", safe=False)
            except IndexError:
                return JsonResponse("Volume doesn't exist!", safe=False)

        if 'MOVEMOTOR' in request.POST:
            
            zMov = volumeToZMovement(float(request.POST['MOVEMOTOR']),False)
            print(zMov)
            mm_movement = round(37-zMov, 2)
            print(mm_movement)
            OC_LAB.send(f"G1Z{mm_movement}F3000")
            return JsonResponse("Volume save", safe=False)

class Cleaning(object):

    def __init__(self):
        self.time_window = 1  # Minimun time for each frequency 5 sec
        self.duration = 0
        self.lines_left = 0

    def dinamic_cleaning(self, fi, fo, step, pressure):
        # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
        # range(start, stop, step)
        self.duration = 0
        dinamic_clean = []
        for i in range(fi, fo + step, step):
            for j in range(1, self.time_window * i + 1):
                dinamic_clean.append(f'G98 F{i}' + '\n')
                if j % 10 == 0:
                    dinamic_clean.append(f'G97 P{pressure}\n')
                self.lines_left += 1
            self.duration += self.time_window
        return dinamic_clean

    def static_cleaning(self, volume, speed):
        # Gcode to move the Pump for a specific volume from 0-position
        # zMovement = round(volume * 58 / 1000, 2)
        generate = GcodeGenerator(True)
        zMovement = volumeToZMovement(volume,True)
        #zIncrement = int(round(zMovement,1)/0.2)
        speed = round(speed * 60, 2)
        generate.homming("XY")
        generate.set_relative()
        generate.toggle_valve()
        # for i in range(zIncrement):
        #     generate.check_pressure()   
        #     generate.linear_move_z(0.2,speed)
        generate.linear_move_z(zMovement, speed)
        generate.wait_ms(500)
        generate.toggle_valve()
        generate.set_absolute()

        print(generate.list_of_gcodes)
        return generate.list_of_gcodes


clean = Cleaning()


class MotorControl(View):
    # Manage the GET request
    def get(self, request):
        return render(
            request,
            "./motorcontrol.html",
            form)


class Clean(View):
    CLEANINGPROCESS_INITIALS = {'start_frequency': 100,
                                'stop_frequency': 500,
                                'steps': 50,
                                'pressure': 15}

    def get(self, request):
        OC_LAB.send('G28XY')
        form['CleaningProcessForm'] = CleaningProcessForm(initial=CLEANINGPROCESS_INITIALS)
        return render(
            request,
            "./cleanprocess.html",
            form)

    def post(self, request):
        if 'cycles' in request.POST:
            for i in range(0, int(request.POST['cycles'])):
                OC_LAB.send('M42 P63 T')
        return render(
            request,
            "./cleanprocess.html",
            {**form})


clean = Cleaning();


class StaticPurge(View):
    def post(self, request):
        if request.POST.get('rinse_volume'):
            gcode = clean.static_cleaning(float(request.POST.get('rinse_volume')),float(request.POST.get('rinse_speed')))
            OC_LAB.print_from_list(gcode)
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})


class CleanControl(View):
    def post(self, request):
        if 'PROCESS' in request.POST:
            clean_param = CleaningProcessForm(request.POST)

            if clean_param.is_valid():
                clean_param = clean_param.cleaned_data
                gcode = clean.dinamic_cleaning(clean_param['start_frequency'],
                                               clean_param['stop_frequency'],
                                               clean_param['steps'],
                                               clean_param['pressure'])

                OC_LAB.print_from_list(gcode)

                data = {'message': f'Cleaning process in progress, please wait! \n'}
                data.update({'duration': clean.duration})
            else:
                data = {'message': 'ERROR'}
                print(clean_param.errors)
            return JsonResponse(data)

        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message': 'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message': 'paused'})

    def get(self, request):
        # Check the status
        if 'checkstatus' in request.GET:
            data = {'busy': 'true',
                    'message': '',
                    }
            if OC_LAB.printing:
                data['message'] = f'Cleaning process in progress, please wait! \n'
                return JsonResponse(data)
            else:
                data['busy'] = 'false'
                data['message'] = 'Done!'
                return JsonResponse(data)


class GcodeEditor(View):

    def get(self, request):
        form['list_load'] = GcodeFile.objects.filter(uploader=request.user).order_by('-id')

        # LIST LOADING
        if 'LISTLOAD' in request.GET:
            gcodefiles = GcodeFile.objects.filter(uploader=request.user).order_by('-id')
            names = [i.filename for i in gcodefiles]
            return JsonResponse(names, safe=False)

        # FILE LOADING
        if 'LOADFILE' in request.GET:
            filename = request.GET.get('filename')
            gcodefile = GcodeFile.objects.filter(uploader=request.user, filename=filename)

            # Open the file
            with open(str(gcodefile[0].gcode), 'r') as f:
                text = f.read()

            response = {'text': text,
                        'filename': gcodefile[0].filename,
                        'success': 'File opened!'}
            return JsonResponse(response)

        return render(
            request,
            "./gcodeeditor.html",
            form)


    def post(self, request):
        # print(request.POST)
        if 'UPLOAD' in request.POST:
            if request.FILES['file']:
                uploaded_file = request.FILES['file']

                if GcodeFile.objects.filter(filename=uploaded_file, uploader=request.user):
                    return JsonResponse({'danger': 'Filename already exist, change it!'})

                if 'gcode' in uploaded_file.content_type:
                    fs = FileSystemStorage('media/gfiles/')
                    new_name = fs.save(uploaded_file.name, uploaded_file)

                    gcode = GcodeFile()
                    gcode.filename = uploaded_file.name;
                    gcode.gcode = fs.location + '/' + new_name;
                    gcode.gcode_url = fs.url(new_name)
                    gcode.uploader = request.user
                    gcode.save()
                    return JsonResponse({'success': 'File Saved!'})
                else:
                    print('entro al else')
                    return JsonResponse({'danger': 'Invalid File'})
            else:
                return JsonResponse({'danger': 'Please select a File'})

        # SAVE FILE
        if 'SAVE' in request.POST:

            filename = request.POST.get('name')
            text = request.POST.get('text')
            fs = FileSystemStorage('media/gfiles/')
            gcodefile = GcodeFile.objects.filter(uploader=request.user, filename=filename)

            # if the file exist then edit
            if gcodefile:
                # Get realitve path from app folder so that can be opened
                path_rel = os.path.relpath(str(gcodefile[0].gcode), '/app/')
                with open(path_rel, 'w+') as f:
                    myfile = File(f)
                    myfile.write(text)
                    new_name = fs.save(filename + '.gcode', content=myfile)
                return JsonResponse({'info': f'{filename} edited'})

            # Create the file
            with open(f'last.gcode', 'w+') as f:
                myfile = File(f)
                myfile.write(text)
                new_name = fs.save(filename + '.gcode', content=myfile)

                gcode = GcodeFile()
                gcode.filename = filename;
                gcode.gcode = fs.location + '/' + new_name;
                gcode.gcode_url = fs.url(new_name)
                gcode.uploader = request.user
                gcode.save()
                return JsonResponse({'success': 'File Saved!'})

        # REMOVE FILE
        if 'REMOVE' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse({'warning': 'Choose a file!'})

            try:
                file = GcodeFile.objects.get(filename=filename, uploader=request.user)
                file.delete()
            except:
                return JsonResponse({'warning': 'Something went wrong!'})

            return JsonResponse({'success': 'File removed!'})

        # RUN FILE
        if 'START' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse({'warning': 'First save the file and Open it!'})
            try:
                file = GcodeFile.objects.get(filename=filename, uploader=request.user)
                if file:
                    with open(f'{file.gcode}', 'r') as f:
                        OC_LAB.print_from_file(f)
                        return JsonResponse({'success': 'Printing!'})
            except DoesNotExist:
                return JsonResponse({'danger': 'File Not Found'})

        # STOP FILE
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'danger': 'STOP'})

class Temperature(View):
    # Manage the GET request
    def get(self, request):
        return render(
            request,
            "./temperature.html",
            form)

class TempControl(View):
    def post(self, request):
        generate = GcodeGenerator(True)
        active=request.POST.get('active')
        if (active=='On'):
            generate.hold_bed_temperature(request.POST.get('temp'))
            generate.report_bed_temperature(4)
        elif (active=='Off'): 
            generate.hold_bed_temperature(0)
            generate.report_bed_temperature(0)
        OC_LAB.print_from_list(generate.list_of_gcodes)
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})

class Fan(View):
    # Manage the GET request
    def get(self, request):
        return render(
            request,
            "./fancontrol.html",
            form)
