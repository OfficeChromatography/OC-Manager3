from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db
from .forms import SampleApplicationForm
# Create your views here.

class Sample(View):

    def get(self, request):
        form = {
            'SampleApplicationForm': SampleApplicationForm(),
        }
        
        return render(request,'sample.html',form)


    def post(self, request):
        return render(request,'sample.html',{})

class Sample_Save(View):

    def post(self, request):
        f = SampleApplicationForm(request.POST)
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
