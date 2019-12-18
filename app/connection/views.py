from django.shortcuts import render
from django.http import HttpResponse

import serial
import serial.tools.list_ports


def connection_view(request, *args, **kwargs):
    ports = serial.tools.list_ports.comports() # List of ports available
    my_context = {
        "My_text": "This is about me",
        "My_number" : 123,
        "My_list": [123,1234,123,1235],
        'object': ports
    }
    return render(request, "connection.html", my_context)
