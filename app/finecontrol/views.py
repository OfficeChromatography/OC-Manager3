from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from connection.views import my_context , Arduino_Port
from connection.serialarduino import ArdComm
from django.core.files.storage import FileSystemStorage
from app.settings import STATIC_ROOT, BASE_DIR, MEDIA_ROOT

from connection.forms import ConnectionForm, ChatForm

# IMPORTS FOR CLASS BASED View
from connection.forms import ChatForm
from connection.models import Connection_Db
from django.views import View
from django.http import JsonResponse


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


# Really New Code
def update_monitor():
    actual_text = Connection_Db.objects.last().chattext
    return actual_text

def validate_username(request):
    username = request.GET.get('commandsend', None)
    print()
    return JsonResponse(data)

class MotorControl_test(View, ):

    context = {
        'commandsend'  : ChatForm(),
        'monitor': ""
    }

    def get(self, request):
        self.context['monitor'] = update_monitor()
        return render(request, "motor_test.html", self.context)

    def post(self, request):
        print("dasdsa")
        if 'chattext' in request.POST:
            self.context['commandsend'] = ChatForm(request.POST)
            if self.context['commandsend'].is_valid():
                self.context['commandsend'].send()
                self.context['monitor'] = update_monitor()
                self.context['commandsend'] = ChatForm()

        return render(request, "motor_test.html", self.context)
