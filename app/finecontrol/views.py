# IMPORTS FOR CLASS BASED View
from connection.forms import ChatForm, OC_LAB
from connection.models import Connection_Db
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core import serializers
from .forms import CleaningProcessForm
from .models import GcodeFile
from printrun import printcore, gcoder
import time

form = {
    'commandsend' : ChatForm()
}

CLEANINGPROCESS_INITIALS = {'start_frequency':100,
            'stop_frequency':500,
            'steps':50,
            'pressure':200}


class Cleaning(object):

    def __init__(self):
        self.time_left = 0
        self.time_window = 5 # Minimun time for each frequency 5 sec
        self.duration = 0
        # self._lastcheck = time.now()

    def dinamic_cleaning(self,fi,fo,step,pressure):
        # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
        # range(start, stop, step)
        self.duration = 0
        f = open("dinamic_clean.gcode", "w+")
        f.write(f'G94 P{pressure}')
        for i in range(fi,fo+step,step):
            for j in range(1,self.time_window*i+1):
                f.write(f'G97 F{i} P{pressure}'+'\n')
            f.write('G94 P0\n')
            self.duration += self.time_window
        f.close()
        self.duration*=1.2 # Error correction
        self.time_left = self.duration

    def read_cleaning_file(self):
        return [code_line.strip() for code_line in open(f'{fs.location}/{new_name}')]

    def remain_time(self):
        self.time_left-=3
        return self.time_left

class MotorControl(View):
    # Manage the GET request
    def get(self, request):
        return render(
            request,
            "./motorcontrol.html",
            form)

    def post(self, request):
        # Steps follow after a message is Send (Monitor send Form)
        if 'chattext' in request.POST:
            form['commandsend'] = ChatForm(request.POST)
            if form['commandsend'].is_valid():
                form['commandsend'].send()
            return JsonResponse({})

        if 'speedrange' in request.POST:
            print(request.POST)
            # Converts the request into a valid gcode
            gcode = simple_move_Gcode_gen(request)
            form['commandsend'] = ChatForm({'chattext': gcode})
            if form['commandsend'].is_valid():
                form['commandsend'].send()
                return JsonResponse({})

class PumpControl(View):

    CLEANINGPROCESS_INITIALS = {'start_frequency':100,
                'stop_frequency':500,
                'steps':50,
                'pressure':200}

    def get(self, request):
        form['CleaningProcessForm'] = CleaningProcessForm(initial=CLEANINGPROCESS_INITIALS)
        return render(
            request,
            "./pumpcontrol.html",
            form)

    def post(self, request):
        if 'cycles' in request.POST:
            for i in range(0,int(request.POST['cycles'])):
                OC_LAB.send('M42 P63 T')
                time.sleep(3/5)
        return render(
            request,
            "./pumpcontrol.html",
            {**form})

clean = Cleaning();

class CleanControl(View):

    def post(self, request):
        print(request.POST)
        if 'PROCESS' in request.POST:
            clean_param = CleaningProcessForm(request.POST)

            if clean_param.is_valid():
                clean_param = clean_param.cleaned_data
                clean.dinamic_cleaning(clean_param['start_frequency'],clean_param['stop_frequency'],clean_param['steps'],clean_param['pressure'])

                gcode = [code_line.strip() for code_line in open('dinamic_clean.gcode')]
                light_gcode = gcoder.LightGCode(gcode)
                OC_LAB.startprint(light_gcode)

                data= {'message':f'Cleaning process in progress, please wait! \n Approx. time left {clean.remain_time()} sec'}
                data.update({'duration':clean.duration})
            else:
                data = {'message':'ERROR'}
                print(clean_param.errors)
            return  JsonResponse(data)

    def get(self, request):
        # Check the status
        if 'checkstatus' in request.GET:
            data = {    'busy':'true',
                        'message':'',
                        }
            if clean.time_left>=0:
                data['message'] = f'Cleaning process in progress, please wait! \n Approx. time left {clean.remain_time()}s'
                data.update({'duration':clean.duration})
                data.update({'time_left':clean.time_left})
                return  JsonResponse(data)
            else:
                data['busy']='false'
                data['message']='Done!'
                data.update({'duration':clean.duration})
                data.update({'time_left':clean.time_left})
                return  JsonResponse(data)

        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message':'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message':'paused'})

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
            gcodefile = GcodeFile.objects.filter(uploader=request.user,filename=filename)


            #Open the file
            with open(gcodefile[0].gcode.path,'r') as f:
                text = f.read()

            response = {'text':text,
                        'filename':gcodefile[0].filename,
                        'success':'File opened!'}
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

                if GcodeFile.objects.filter(filename=uploaded_file,uploader=request.user):
                    return JsonResponse({'danger':'Filename already exist, change it!'})

                if 'gcode' in uploaded_file.content_type:
                    fs = FileSystemStorage('media/gfiles/')
                    new_name = fs.save(uploaded_file.name, uploaded_file)

                    gcode = GcodeFile()
                    gcode.filename = uploaded_file.name;
                    gcode.gcode = fs.location+'/'+new_name;
                    gcode.gcode_url = fs.url(new_name)
                    gcode.uploader = request.user
                    gcode.save()
                    return JsonResponse({'success':'File Saved!'})
                else:
                    print('entro al else')
                    return JsonResponse({'danger':'Invalid File'})
            else:
                return JsonResponse({'danger':'Please select a File'})


        # SAVE FILE
        if 'SAVE' in request.POST:

            filename = request.POST.get('name')
            text = request.POST.get('text')
            fs = FileSystemStorage('media/gfiles/')
            gcodefile = GcodeFile.objects.filter(uploader=request.user,filename=filename)

            # if the file exist then edit
            if gcodefile:
                with open(gcodefile[0].gcode.path,'w+') as f:
                    myfile = File(f)
                    myfile.write(text)
                    new_name = fs.save(filename+'.gcode',content=myfile)
                return JsonResponse({'info':f'{filename} edited'})


            # Create the file
            with open(f'last.gcode','w+') as f:
                myfile = File(f)
                myfile.write(text)
                new_name = fs.save(filename+'.gcode',content=myfile)


                gcode = GcodeFile()
                gcode.filename = filename;
                gcode.gcode = fs.location+'/'+new_name;
                gcode.gcode_url = fs.url(new_name)
                gcode.uploader = request.user
                gcode.save()
                return JsonResponse({'success':'File Saved!'})

        # REMOVE FILE
        if 'REMOVE' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse({'warning':'Choose a file!'})

            try:
                file = GcodeFile.objects.get(filename=filename,uploader=request.user)
                file.delete()
            except:
                return JsonResponse({'warning':'Something went wrong!'})


            return JsonResponse({'success':'File removed!'})

        # RUN FILE
        if 'START' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse({'warning':'First save the file and Open it!'})
            try:
                file = GcodeFile.objects.get(filename=filename,uploader=request.user)
                if file:
                    with open(f'{file.gcode}','r') as f:
                        lines_gcode = [code_line.strip() for code_line in f]
                        light_gcode = gcoder.LightGCode(lines_gcode)
                        OC_LAB.startprint(light_gcode)
                        return JsonResponse({'success':'Printing!'})
            except DoesNotExist:
                return JsonResponse({'danger':'File Not Found'})

        # STOP FILE
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'danger':'STOP'})



def simple_move_Gcode_gen(request):
    direction = request.POST.get('button')
    speed = request.POST.get('speedrange')
    step = request.POST.get('steprange')
    if 'arrow' in direction:
        gcode = "G1 "
        if 'left' in direction:
            gcode += "X-"
        elif 'right' in direction:
            gcode += "X"
        elif 'down' in direction:
            gcode += "Y-"
        else:
            gcode += "Y+"
        gcode += str(step)
    if 'homming' in direction:
        gcode = "G28 "
        if 'x' in direction:
            gcode += 'X'
        else:
            gcode += 'Y'
    return gcode + ' F' + str(speed)


def static_cleaning():
    # THE GCODE TO PUMP NO MATTER THE PRESSURE
    gcode = ''
    # OPEN DE VALVE AND LEAVE IT LIKE THAT
    f = open("static_clean.gcode", "w+")
    for i in range(0,100):
        f.write(gcode+f'{i}'+'\n')
    f.close()
