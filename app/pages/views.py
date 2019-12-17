from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "index.html",{})

def connection_view(request, *args, **kwargs):
    my_context = {
        "My_text": "This is about me",
        "My_number" : 123
    }
    return render(request, "connection.html", my_context)

def axis_view(request, *args, **kwargs):
    return render(request, "axis.html",{})

def method_view(request, *args, **kwargs):
    return render(request, "404.html",{})

def motorcontrol_view(request, *args, **kwargs):
    return render(request, "motorcontrol.html",{})

def documentation_view(request, *args, **kwargs):
    return render(request, "documentation.html",{})

def inkjet_view(request, *args, **kwargs):
    return render(request, "inkjet.html",{})
