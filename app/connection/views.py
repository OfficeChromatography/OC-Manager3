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

    ports = serial.tools.list_ports.comports()
    my_context['object']=ports
    if request.method == 'POST':
        selected = request.POST.get('port_selected')
        if selected == "Choose...":
            my_context['message']="Please select port"
            my_context['connected'] = False
        else:
            connectArduino(selected)
            my_context['message'] = "Connected to " + selected
            my_context['connected'] = True
            my_context['device'] = selected
        # if "_send" in request.POST:
            # ser.write(bytes(b''+'))
    return render(request, "connection.html", my_context)

def connectArduino(port):
    closeArduino()
    # Connect to selected port
    ser.port=port;
    ser.open()
    my_context['baudrate']=ser.baudrate
    readArduino()
    return

def closeArduino():
    # Close any posible connection and clean the monitor
    ser.close()
    my_context['received'] = ""
    return

def readArduino(): # Read 1 sec mssg
    timeout = 1  # [seconds]
    timeout_start = time.time()
    while time.time() < timeout_start+timeout:
        ser_bytes = ser.read_until() #(‘\n’ by default)
        decoded_bytes = ser_bytes[0:len(ser_bytes)-1].decode("utf-8")
        my_context['received']+=str(decoded_bytes)+str('\n')
    return

# def read(){
#     if(ser.in_waiting != 0):
#
# }
