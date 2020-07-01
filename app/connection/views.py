from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ConnectionForm, ChatForm, OC_LAB


# MainView of Connection
class Connection_test(View):

    def get(self, request):
        form = {
            'connectionset': ConnectionForm(initial={
                                'baudrate': '115200',
                                'timeout': '2',
                                }),
            'commandsend': ChatForm(),
        }
        return render(
                        request,
                        "connection.html",
                        form
                        )

    def post(self, request):
        # Steps follow after a ConnectionRequest is Send (Connection Form)

        if 'oc_lab' in request.POST:
            connection_form_instance = ConnectionForm(request.POST, user=request.user)
            if connection_form_instance.is_valid():
                data = IsConnected.data_info()
                connection_form_instance.save()
            else:
                data = IsConnected.data_info()
            return JsonResponse({**data})

        # Steps follow after a message was sent (Monitor send Form)
        if 'chattext' in request.POST:
            commandsend = ChatForm(request.POST)
            if commandsend.is_valid():
                commandsend.send()
            return JsonResponse({})

# EndPoint to Know if theres a current connection with an OC-Lab
class IsConnected(View):
    def get(self, request):
        return JsonResponse(self.data_info())

    @staticmethod
    def data_info():
        device={}
        device['connected'] = (OC_LAB.printer != None)
        device['port'] = OC_LAB.port
        device['baudrate'] = OC_LAB.baud
        return device
