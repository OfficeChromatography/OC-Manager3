from django.shortcuts import render
from .serialarduino import ArdComm
from .forms import ConnectionForm, ChatForm
from .models import Connection_Db
from django.views import View


Arduino_Port = ArdComm(baudrate=115200, timeout=1)

my_context = {
    'object': [],
    'message': "",
    'connected': "False",
    'device': "",
    'baudrate': "",
    'received': "",
    'errormsg': "",
}

context = {
    'connectionset': ConnectionForm(initial={'baudrate':'115200', 'timeout':'2'}),
    'commandsend'  : ChatForm(),
    'monitor': "",
    'device': '',
    'connected': 'False',
    'baudrate': '',
}


def update_monitor(**kwargs):
    if context['connected'] == 'True':
        actual_text = Connection_Db.objects.last().chattext
    else:
        actual_text = ''
    return actual_text

def get_device():
    return Connection_Db.objects.last().oc_lab

def get_baudrate():
    return Connection_Db.objects.last().baudrate

# Really New Code


class Connection_test(View):

    def get(self, request):
        self.update_parameters()
        context['connectionset']    =  context['connectionset']
        return render(request, "connection.html", context)

    def post(self, request):
        if ('oc_lab' in request.POST):
            context['connectionset'] = ConnectionForm(request.POST)
            context['monitor'] = ""
            if context['connectionset'].is_valid():
                context['connectionset'].connect()
                self.update_parameters(connected='True')
        else:
            context['commandsend'] = ChatForm(request.POST)
            if context['commandsend'].is_valid():
                context['commandsend'].send()
                self.update_parameters()
                context['commandsend'] = ChatForm()
        return render(request, "connection.html", context)

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            context[key] = value
        context['connectionset'].update()
        context['monitor'] = update_monitor()
        context['device']  = get_device()
        context['baudrate']  = get_baudrate()
