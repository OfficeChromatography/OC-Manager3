from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ConnectionForm, ChatForm, OC_LAB


# Some inital DATA
form = {
    'connectionset': ConnectionForm(initial={
                        'baudrate': '115200',
                        'timeout': '2',
                        }),
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

# MainView of Connection
class Connection_test(View):

    def get(self, request):
        form['connectionset'].update()
        return render(
                        request,
                        "connection.html",
                        {**state, **form, **data}
                        )

    def post(self, request):
        # Steps follow after a ConnectionRequest is Send (Connection Form)
        if 'oc_lab' in request.POST:
            connection_form_instance = ConnectionForm(request.POST, user=request.user)
            if connection_form_instance.is_valid():
                data = {
                    'connected':True,
                    'device': connection_form_instance.cleaned_data['oc_lab'],
                    'baudrate': connection_form_instance.cleaned_data['baudrate'],
                }
                connection_form_instance.save()
            else:
                print(connection_form_instance.errors)
            return JsonResponse({**state, **data})

        # Steps follow after a message is Send (Monitor send Form)
        if 'chattext' in request.POST:
            form['commandsend'] = ChatForm(request.POST)
            if form['commandsend'].is_valid():
                form['commandsend'].send()
            return JsonResponse(data)

# EndPoint to Know if theres a current connection to an OC-Lab
class IsConnected(View):
    def get(self, request):
        info={}
        info['port'] = OC_LAB.port
        if OC_LAB.port:
            info['connected'] = True
        return JsonResponse(info)
