from django.shortcuts import render
# IMPORTS FOR CLASS BASED View
from connection.forms import ChatForm, OC_LAB
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core import serializers
from printrun import printcore, gcoder
import time


class DevelopmentControl(View):
    # Manage the GET request
    def get(self, request):
        return render(
            request,
            "./development.html",
            {})

    def post(self, request):
        # Steps follow after a message is Send (Monitor send Form)
        if 'chattext' in request.POST:
            form['commandsend'] = ChatForm(request.POST)
            if form['commandsend'].is_valid():
                form['commandsend'].send()
            return JsonResponse({})

        if 'speedrange' in request.POST:
            print(request.POST)
            # Converts the request into a valid gcode
            gcode = simple_move_Gcode_gen(request)
            form['commandsend'] = ChatForm({'chattext': gcode})
            if form['commandsend'].is_valid():
                form['commandsend'].send()
                return JsonResponse({})
