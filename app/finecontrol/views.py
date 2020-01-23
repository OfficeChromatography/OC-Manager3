from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from connection.views import my_context , Arduino_Port
from connection.serialarduino import ArdComm
from django.core.files.storage import FileSystemStorage
from app.settings import STATIC_ROOT, BASE_DIR, MEDIA_ROOT

import os
# Create your views here.
@csrf_exempt
def motorcontrol_view(request, *args, **kwargs):
    error = "Please, go to Connection and connect the Arduino"
    my_context['gcode_url'] = ""
    if request.method == 'POST':
        if 'left_arrow' in request.POST:
            try:
                move = 'G1 X10'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'right_arrow' in request.POST:
            try:
                move = 'G1 X-10'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'x_homming' in request.POST:
            try:
                move = 'M28 X'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'up_arrow' in request.POST:
            try:
                move = 'G1 Y10'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'down_arrow' in request.POST:
            try:
                move = 'G1 Y-10'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'y_homming' in request.POST:
            try:
                move = 'M28 Y'
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error

        if 'Gcode' in request.POST:
            try:
                move = request.POST.get('Gcode')
                my_context['received'] += Arduino_Port.writeArduino(move)
            except:
                my_context['errormsg'] = error
        if 'document' in request.FILES:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            my_context['gcode_url'] = fs.url(name)
            my_context['gcode_filename'] = uploaded_file
    return render(request, "./motorcontrol.html", my_context)
