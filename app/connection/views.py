from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ConnectionForm, OC_LAB


# MainView of Connection
class Connection_test(View):
    def get(self, request):
        form = {
            'connectionset': ConnectionForm(initial={
                                'baudrate': '115200',
                                'timeout': '2',
                                }),
        }
        return render(
                        request,
                        "connection.html",
                        form
                        )

    def post(self, request):
        print(request.POST)
        # Steps follow after a ConnectionRequest is Send (Connection Form)
        if 'oc_lab' in request.POST:
            connection_form_instance = ConnectionForm(request.POST, user=request.user)
            if connection_form_instance.is_valid():
                data = IsConnected.data_info()
                connection_form_instance.save()
            else:
                data = IsConnected.data_info()
            return JsonResponse({**data})

        if 'DISCONNECT' in request.POST:
            if OC_LAB:
                OC_LAB.disconnect();
                return JsonResponse({'message':'disconnected'})


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

class CommunicationWithOC(View):
    def post(self,request):
        gcode = request.POST.get('gcode')
        OC_LAB.send(gcode)
        return JsonResponse({'message':'Message sent'})
