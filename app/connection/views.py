from django.shortcuts import render
from django.http import HttpResponse
from .serialarduino import ArdComm

import serial.tools.list_ports
import time

Arduino_Port = ArdComm(baudrate=115200, timeout=1)

my_context = {
    'object': "",
    'message': "",
    'connected': False,
    'device': "",
    'baudrate': "",
    'received': "",
}
def connection_view(request):
    my_context['object'] = serial.tools.list_ports.comports()
    if request.method == 'POST':

        if 'port_selected' in request.POST:
            selected = request.POST.get('port_selected')

            if selected == "Choose...":
                my_context['message'] = "Please select port"
                my_context['connected'] = False
            else:
                Arduino_Port.closeArduino()
                my_context['received'] = ""
                Arduino_Port.connectArduino(selected)
                my_context['baudrate'] = Arduino_Port.baudrate
                my_context['device'] = Arduino_Port.name
                my_context['message'] = "Connected to " + my_context['device']
                my_context['connected'] = True
                my_context['received'] += Arduino_Port.readArduino()

        if "usermsg" in request.POST:
            Arduino_Port.writeArduino(request.POST.get("usermsg"))
            my_context['received'] += request.POST.get("usermsg")+'\n'
            my_context['received'] += Arduino_Port.readArduino()

    return render(request, "connection.html", my_context)
