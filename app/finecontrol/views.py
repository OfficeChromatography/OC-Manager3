from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from connection.views import my_context , Arduino_Port
from connection.serialarduino import ArdComm

# Create your views here.
@csrf_exempt
def motorcontrol_view(request, *args, **kwargs):
    error = "Please, go to Connection and connect the Arduino"

    if request.method == 'POST':
        if 'left_arrow' in request.POST:
            try:
                move = 'G1 X10'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'right_arrow' in request.POST:
            try:
                move = 'G1 -X10'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'x_homming' in request.POST:
            try:
                move = 'M28 X'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'up_arrow' in request.POST:
            try:
                move = 'G1 Y10'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'down_arrow' in request.POST:
            try:
                move = 'G1 -Y10'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'y_homming' in request.POST:
            try:
                move = 'M28 Y'
                my_context['received'] += Arduino_Port.writeArduino(move)
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error

        if 'Gcode' in request.POST:
            try:
                move = request.POST.get('Gcode')
                Arduino_Port.writeArduino(move)
                my_context['received'] += move+'\n'
                my_context['received'] += Arduino_Port.readArduino()
            except:
                my_context['errormsg'] = error
    return render(request, "./motorcontrol.html", my_context)
