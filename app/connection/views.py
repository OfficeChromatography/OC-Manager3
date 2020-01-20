from django.shortcuts import render
# from django.http import HttpResponse
from .serialarduino import ArdComm
# import time

Arduino_Port = ArdComm(baudrate=115200, timeout=1)

my_context = {
    'object': [],
    'message': "",
    'connected': "False",
    'device': "",
    'baudrate': "",
    'received': "",
    'errormsg': "",
    'busy': 'false'
}
blank = my_context


def connection_view(request):
    if request.method == 'GET':
        my_context['object'] = []
        my_context['object'] = ArdComm.ArduinosConnected()
        if not my_context['object']:
            Arduino_Port.closeArduino()
            for i in my_context:
                my_context[i]=""
            my_context['connected']= "False"

    if request.method == 'POST':
        error=0
        if 'port_selected' in request.POST:
            selected = request.POST.get('port_selected')
            if selected == "Choose...":
                my_context['message'] = "Please select port"
                my_context['connected'] = "False"
            else:
                my_context['received'] = ""
                error = 0
                while my_context['received'] == "" and error<19:
                    try:
                        my_context['busy'] = 'true'
                        Arduino_Port.closeArduino()
                        Arduino_Port.connectArduino(selected)
                        my_context['received'] += Arduino_Port.readArduino()
                        my_context['baudrate'] = Arduino_Port.baudrate
                        my_context['device'] = Arduino_Port.name
                        my_context['message'] = "Connected to " + my_context['device']
                        my_context['connected'] = "True"
                        my_context['busy'] = 'false'
                    except:
                        my_context['errormsg'] = "Connection Error 1"
                        error+=1
                        print(error)
        if "usermsg" in request.POST:
            my_context['busy'] = 'true'
            my_context['received'] += Arduino_Port.writeArduino(request.POST.get("usermsg"))
            my_context['received'] += Arduino_Port.readArduino()
            my_context['busy'] = 'false'
    return render(request, "connection.html", my_context)
