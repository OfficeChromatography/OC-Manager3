from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db
from .forms import SampleApplicationForm
from django.forms.models import model_to_dict
import json



# Create your views here.

class Sample(View):

    def get(self, request):
        form = {
            'SampleApplicationForm': SampleApplicationForm(user=request.user),
        }
        form['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user)
        return render(request,'sample.html',form)
    def post(self, request):
        return render(request,'sample.html',{})

class Sample_EndPoint(View):
    def post(self, request):
        f = SampleApplicationForm(request.POST, user=request.user)
        if f.is_valid():
            new_plateproperties = PlateProperties_Db(**f.plate_properties)
            new_plateproperties.save()
            new_bandsettings = BandSettings_Db(**f.band_settings)
            new_bandsettings.save()
            new_sampleapp = f.save(commit=False)
            new_sampleapp.auth_id = request.user
            new_sampleapp.filename = request.POST.get('filename')
            new_sampleapp.plateproperties = new_plateproperties
            new_sampleapp.bandsettings = new_bandsettings
            new_sampleapp.save()
        return JsonResponse({'error':f.errors})

    def get(self, request):
        filename=request.GET.get('filename')

        sampleapplication_conf=model_to_dict(SampleApplication_Db.objects.filter(filename=filename).filter(auth_id=request.user)[0])
        plateproperties_conf=model_to_dict(PlateProperties_Db.objects.get(id=sampleapplication_conf['plateproperties']))
        bandsettings_conf=model_to_dict(BandSettings_Db.objects.get(id=sampleapplication_conf['bandsettings']))

        sampleapplication_conf.update(plateproperties_conf)
        sampleapplication_conf.update(bandsettings_conf)

        print(sampleapplication_conf)
        return JsonResponse(sampleapplication_conf)
