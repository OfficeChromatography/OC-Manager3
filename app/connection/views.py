from django.shortcuts import render
from django.http import HttpResponse

import serial
import serial.tools.list_ports
import time

ser = serial.Serial(baudrate=115200, timeout=1)

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
                my_context['message']="Please select port"
                my_context['connected'] = False
            else:
                connectArduino(selected)

        if "usermsg" in request.POST:
            writeArduino(request.POST.get("usermsg"))
    return render(request, "connection.html", my_context)

def connectArduino(port):
    closeArduino()
    # Connect to selected port
    ser.port=port;
    ser.open()
    my_context['baudrate'] = ser.baudrate
    my_context['message'] = "Connected to " + port
    my_context['connected'] = True
    my_context['device'] = port
    readArduino()
    return

def closeArduino():
    # Close any posible connection and clean the monitor
    ser.close()
    my_context['received'] = ""
    return

def readArduino(): # Read 1 sec mssg
    while True:
        ser_bytes = ser.read_until() #(‘\n’ by default)
        decoded_bytes = ser_bytes[:-1].decode("utf-8")
        my_context['received']+=str(decoded_bytes)+str('\n')
        if my_context['received'][-1]=='\n' and my_context['received'][-2]=='\n':
            # my_context['received']=my_context['received'][:-1]
            break
    return

def writeArduino(menssage):
    menssage+=2*'\n'
    my_context['received']+=menssage
    ser.write(menssage.encode('utf-8'))
    readArduino()
    return
