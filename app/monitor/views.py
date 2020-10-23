from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Monitor_Db
from connection.views import IsConnected

def monitor(request):
    return render(request, 'chat.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

class MonitorView(View):
    def get(self, request):
        monitor = Monitor_Db.objects.last()
        response = {'monitortext':monitor.monitortext}
        response.update(IsConnected.data_info())
        return JsonResponse(response)
