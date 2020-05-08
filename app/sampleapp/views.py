from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SampleAppForm
# Create your views here.

class Sample(FormView):
    def get(self, request):
        form = {
            'SampleAppForm': SampleAppForm(),
        }
        # form['list_load'] = SampleApplication_Db.objects.filter(auth_id=request.user)
        return render(request,'sample2.html',form)
    def post(self, request):
        return render(request,'sample2.html',{})

class SampleAppPlay(View):
    def get(self, request):
        return render(request,'sample2.html',form)
    def post(self, request):
        f = SampleAppForm(request.POST)
        print(request.POST)
        if f.is_valid():
            motor_speed = int(f.cleaned_data['motor_speed'])
            delta_x = int(f.cleaned_data['delta_x'])
            delta_y = int(f.cleaned_data['delta_y'])

            size_x = int(f.cleaned_data['size_x'])
            size_y = int(f.cleaned_data['size_y'])
            offset_x = int(f.cleaned_data['offset_x'])
            offset_y = int(f.cleaned_data['offset_y'])

            main_property = int(f.cleaned_data['main_property'])
            n_bands = int(f.cleaned_data['n_bands'])
            length = int(f.cleaned_data['length'])
            height = int(f.cleaned_data['height'])
            gap = int(f.cleaned_data['gap'])

            working_area = [size_x-2*offset_x,size_y-2*offset_y]

            # if

            # workingarea = sizexvalue-2*offsetxvalue
            #
            # if bandsetting == 'N° Bands':
            #     bandsize = (workingarea-(gapvalue*(nbands-1)))/nbands
            # else:
            #     floatnbands = (workingarea+gapvalue)/(bandlength+gapvalue)
            #   # Then we get the integer value of bands
            #     nbands = int(floatnbands)
            #   # the fractions of band is added as offsets
            #     leftover = bandlength*(floatnbands%nbands)
            #     offsetxvalue += leftover
            #     bandsize = bandlength
            #
            # if bandsize>=0:
            #     applicationsurface = []
            #     heightofapplication = 0
            #     while heightofapplication < bandheight:
            #         for i in range(0,nbands):
            #             applicationline=[]
            #             if i==0:
            #               applicationline.append([offsetyvalue+heightofapplication, offsetxvalue])
            #               applicationline.append([offsetyvalue+heightofapplication, bandsize+offsetxvalue])
            #             else:
            #               applicationline.append([offsetyvalue+heightofapplication,i*(bandsize+gapvalue)+offsetxvalue])
            #               applicationline.append([offsetyvalue+heightofapplication,(i+1)*bandsize+(gapvalue*i)+offsetxvalue])
            #             # print(applicationline)
            #             applicationsurface.append(applicationline)
            #         heightofapplication+=0.1
            #     # print(applicationsurface)
            #     gcode = GcodeGen(applicationsurface, motorspeed)
            #     print(gcode)
            #     # OC_LAB.send(gcode)

        return JsonResponse({'error':f.errors})
