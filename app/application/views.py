from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db
from .forms import SampleApplicationForm
from django.forms.models import model_to_dict
import json
from django.views.generic import FormView
from connection.forms import ChatForm, OC_LAB
import time

# Create your views here.

class Sample(FormView):
    def get(self, request):
        form = {
            'SampleApplicationForm': SampleApplicationForm(user=request.user),
        }
        form['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user)
        return render(request,'sample.html',form)
    def post(self, request):
        return render(request,'sample.html',{})

class SampleAppSaveAndLoad(View):
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

        # print(sampleapplication_conf)
        return JsonResponse(sampleapplication_conf)

class SampleAppPlay(View):
    def post(self, request):
        f = SampleApplicationForm(request.POST, user=request.user)
        if f.is_valid():
            nbands = int(f.band_settings['nbands'])
            bandlength = float(f.band_settings['lengthbands'])
            bandheight = float(f.band_settings['height'])
            gapvalue = float(f.band_settings['gap'])
            bandsetting = f.band_settings['bandsetting']

            sizexvalue = float(f.plate_properties['sizex'])
            sizeyvalue = float(f.plate_properties['sizey'])
            offsetxvalue = float(f.plate_properties['offsetx'])
            offsetyvalue = float(f.plate_properties['offsety'])


            workingarea = sizexvalue-2*offsetxvalue

            if bandsetting == 'N° Bands':
                bandsize = (workingarea-(gapvalue*(nbands-1)))/nbands
            else:
                floatnbands = (workingarea+gapvalue)/(bandlength+gapvalue)
              # Then we get the integer value of bands
                intnbands = int(floatnbands)
              # the fractions of band is added as offsets
                leftover = bandlength*(floatnbands%intnbands)
                offsetxvalue += leftover
                bandsize = bandlength

            # print(bandsetting)

            if bandsize>=0:
                applicationsurface = []
                heightofapplication = 0
                while heightofapplication < bandheight:
                    for i in range(0,nbands):
                        applicationline=[]
                        if i==0:
                          applicationline.append([offsetyvalue+heightofapplication, offsetxvalue])
                          applicationline.append([offsetyvalue+heightofapplication, bandsize+offsetxvalue])
                        else:
                          applicationline.append([offsetyvalue+heightofapplication,i*(bandsize+gapvalue)+offsetxvalue])
                          applicationline.append([offsetyvalue+heightofapplication,(i+1)*bandsize+(gapvalue*i)+offsetxvalue])
                        applicationsurface.append(applicationline)
                    heightofapplication+=0.1
                gcode = GcodeGen(applicationsurface)
                OC_LAB.send(gcode)
                print(gcode)

        return JsonResponse({'error':f.errors})

class SampleAppStop(View):
    def get(self, request):
        print(request.GET)
        if 'stop' in request.GET:
            print('PARO')
            OC_LAB.cancelprint()
        if 'pause' in request.GET:
            if OC_LAB.printing:
                OC_LAB.pause()
                print('pauso')
            else:
                print(OC_LAB.printing)
                OC_LAB.resume()
                print('resumio')
        return JsonResponse({})

def GcodeGen(listoflines):
    gcode=''
    for listofpoints in listoflines:
        for point in listofpoints:
            gline = 'G1 Y{} X{} \n'.format(str(point[0]), str(point[1]))
            gcode += gline
            gcode += 'M42 P13 S255 \n'
        gcode = gcode[:gcode.rfind('M42 P13 S255 \n')]
        gcode += 'M42 P13 S0 \n' # End of line
    return gcode
