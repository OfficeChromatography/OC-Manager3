# chat/views.py
from django.shortcuts import render

def monitor(request):
    return render(request, 'chat.html', {})
