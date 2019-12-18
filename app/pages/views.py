from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "index.html",{})

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
