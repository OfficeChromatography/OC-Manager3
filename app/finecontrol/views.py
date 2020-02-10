# IMPORTS FOR CLASS BASED View
from connection.forms import ChatForm
from connection.models import Connection_Db
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from connection.views import data, state, form
from django.contrib.auth.mixins import LoginRequiredMixin

def update_monitor(**kwargs):
    return Connection_Db.objects.last().chattext


def get_device():
    return Connection_Db.objects.last().oc_lab


def get_baudrate():
    return Connection_Db.objects.last().baudrate


# class MotorControl(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'login'
class MotorControl(View):

    def get(self, request):
        data['monitor'] = update_monitor()
        return render(
            request,
            "./motorcontrol.html",
            {**form, **data, **state})

    def post(self, request):
        if 'chattext' in request.POST:
            form['commandsend'] = ChatForm(request.POST)
            if form['commandsend'].is_valid():
                if request.POST.get('chattext') == 'CLEAR':
                    data['monitor'] = ""
                else:
                    form['commandsend'].send()
                    self.update_parameters()
                    form['commandsend'] = ChatForm()
            return JsonResponse(data)

        if 'speedrange' in request.POST:
            gcode = simple_move_Gcode_gen(request)
            print(gcode)
            # print(type_of(gcode))
            form['commandsend'] = ChatForm({'chattext': gcode})
            if form['commandsend'].is_valid():
                form['commandsend'].send()
                self.update_parameters()
                form['commandsend'] = ChatForm()
                return JsonResponse(data)
        else:
            return render(
                    request,
                    "./motorcontrol.html",
                    {**form, **data, **state})

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            state[key] = value
        if state['connected'] == 'True':
            form['connectionset'].update()
            data['monitor'] = update_monitor()
            data['device'] = get_device()
            data['baudrate'] = get_baudrate()
        else:
            for i in data:
                data[i] = ''


def simple_move_Gcode_gen(request):
    direction = request.POST.get('button')
    speed = request.POST.get('speedrange')
    step = request.POST.get('steprange')
    if 'arrow' in direction:
        gcode = "G1 "
        if 'left' in direction:
            gcode += "-X"
        elif 'right' in direction:
            gcode += "X+"
        elif 'down' in direction:
            gcode += "-Y"
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
