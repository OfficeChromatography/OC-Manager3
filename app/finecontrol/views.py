# IMPORTS FOR CLASS BASED View
from connection.forms import ChatForm, OC_LAB
from connection.models import Connection_Db
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage

from printrun import printcore
import time

form = {
    'commandsend' : ChatForm()
}

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
            return JsonResponse(data)

        if 'speedrange' in request.POST:
            # Converts the request into a valid gcode
            gcode = simple_move_Gcode_gen(request)
            form['commandsend'] = ChatForm({'chattext': gcode})
            if form['commandsend'].is_valid():
                form['commandsend'].send()
                return JsonResponse(data)

        if request.FILES['GFile']:
            # Upload the Gcode file
            uploaded_file = request.FILES['GFile']
            if 'gcode' in uploaded_file.content_type:
                fs = FileSystemStorage()
                new_name = fs.save(uploaded_file.name, uploaded_file)
                print(f'{fs.location}/{new_name}')
                # with open(f'{fs.location}/{new_name}', 'w') as file:
                #     gcode = [code_line.strip() for code_line in file]
                #     print(gcode)


            return render(
                    request,
                    "./motorcontrol.html",
                    form)
        else:
            return render(
                    request,
                    "./motorcontrol.html",
                    form)

class PumpControl(View):

    def get(self, request):
        return render(
            request,
            "./pumpcontrol.html",
            {**form, **data, **state})

    def post(self, request):
        if 'cycles' in request.POST:
            for i in range(0,int(request.POST['cycles'])):
                OC_LAB.send('M42 P63 T')
                time.sleep(3/5)
        return render(
            request,
            "./pumpcontrol.html",
            {**form, **data, **state})


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
        gcode = "G0 G28 "
        if 'x' in direction:
            gcode += 'X'
        else:
            gcode += 'Y'
    return gcode + ' F' + str(speed)
