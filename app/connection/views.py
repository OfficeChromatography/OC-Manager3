from django.shortcuts import render
from .forms import ConnectionForm, ChatForm, OC_LAB
from .models import Connection_Db
from django.views import View
from django.http import JsonResponse
from accounts.views import USER_INFO
import time

form = {
    'connectionset': ConnectionForm(initial={
                        'baudrate': '115200',
                        'timeout': '2'}),
    'commandsend': ChatForm(),
}

data = {
    'monitor': "",
    'device': '',
    'baudrate': '',
}
state = {
    'connected': 'false',
}

USER_INFO = {

}
def update_monitor(**kwargs):
    return Connection_Db.objects.last().chattext


def get_device():
    return Connection_Db.objects.last().oc_lab


def get_baudrate():
    return Connection_Db.objects.last().baudrate


class Connection_test(View):

    def get(self, request):
        USER_INFO['username']=request.user.get_username()
        self.update_parameters()
        print(data)
        return render(
                        request,
                        "connection.html",
                        {**state, **form, **data}
                        )

    def post(self, request):
        if 'oc_lab' in request.POST:
            form['connectionset'] = ConnectionForm(request.POST)
            data['monitor'] = ""
            if form['connectionset'].is_valid():
                form['connectionset'].connect()
                form['connectionset'].useridentification(request.user)
                self.update_parameters(connected='true')
            return JsonResponse({**state, **data})

        if 'chattext' in request.POST:
            form['commandsend'] = ChatForm(request.POST)
            if 'chattext' in request.POST:
                OC_LAB.send(request.POST['chattext'])
                form['commandsend'] = ChatForm()
            return JsonResponse(data)

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            state[key] = value
        if state['connected'] == 'true':
            form['connectionset'].update()
            data['monitor'] = update_monitor()
            data['device'] = get_device()
            data['baudrate'] = get_baudrate()
        else:
            for i in data:
                data[i] = ''
