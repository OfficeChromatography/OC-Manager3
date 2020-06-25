from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm
from app.settings import STATIC_ROOT
from .models import Images_Db
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import time
import subprocess
from types import SimpleNamespace


INITIALS = {'brightness': 50,
            'contrast': 0,
            'saturation': 0,
            'red_balance': 1000,
            'blue_balance': 1000,
            'sharpness': 0,
            'color_effects': 0,
            'power_line_frequency':1,
            'horizontal_flip':0,
            'vertical_flip':0,
            'rotate':0,
            'color_effects_cbcr':32896,

            'resolution':'1280x720',
            'pixelformat':3,

            'auto_exposure':0,
            'exposure_dynamic_framerate':0,
            'auto_exposure_bias':12,
            'exposure_time_absolute':1000,
            'exposure_metering_mode':0,
            'white_balance_auto_preset':1,
            'image_stabilization':0,
            'iso_sensitivity_auto':1,
            'iso_sensitivity':0,
            'scene_mode':0
            }

# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        # FILE LOADING
        if 'LOADFILE' in request.GET:
            filename = request.GET.get('filename')
            image = Images_Db.objects.filter(uploader=request.user,filename=filename)
            url = image[0].url
            response = {'url':image[0].url,
                        'filename':image[0].filename}
            return JsonResponse(response)

        if 'LISTLOAD' in request.GET:
            images = Images_Db.objects.filter(uploader=request.user).order_by('-id')
            names = [i.filename for i in images]
            return JsonResponse(names, safe=False)

        else:
            form['FormatControlsForm'] = ShootConfigurationForm(initial=INITIALS)
            form['CameraControlsForm'] = CameraControlsForm(initial=INITIALS)
            form['UserControlsForm'] = UserControlsForm(initial=INITIALS)
            form['list_load'] = Images_Db.objects.filter(uploader=request.user).order_by('-id')

            data={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
            return render(
                            request,
                            "capture.html",
                            {**form, **data}
                            )

    def post(self, request):
        print(request.POST)
        # SAVE IMAGE
        if 'SAVE' in request.POST:
            filename = request.POST['filename'];

            if Images_Db.objects.filter(filename=filename,uploader=request.user):
                return JsonResponse({'danger':'Filename already exist, change it!'})

            image = Images_Db()
            image.filename = filename
            image.url = request.POST['url'];
            image.uploader = request.user
            image.save()
            return JsonResponse({'success':'File saved!'})

        if 'REMOVE' in request.POST:
            # print(request.POST)
            filename = request.POST.get('filename')
            try:
                file = Images_Db.objects.get(filename=filename,uploader=request.user)
                file.delete()
            except:
                return JsonResponse({'warning':'Something went wrong!'})
            return JsonResponse({'success':'File removed!'})

        else:
            form['FormatControlsForm'] = ShootConfigurationForm(request.POST or None)
            form['CameraControlsForm'] = CameraControlsForm(request.POST or None)
            form['UserControlsForm'] = UserControlsForm(request.POST or None)

            data={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
            if form['CameraControlsForm'].is_valid():
                for key, value in form['CameraControlsForm'].cleaned_data.items():
                    # print(f'{key}={value}')
                    subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
            else:
                print(form['CameraControlsForm'].errors)


            if form['UserControlsForm'].is_valid():
                for key, value in form['UserControlsForm'].cleaned_data.items():
                    # print(f'{key}={value}')
                    subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
            else:
                print('Error user Control')

            if form['FormatControlsForm'].is_valid():
                conf = form['FormatControlsForm'].cleaned_data

                width = conf['resolution'][0]
                height = conf['resolution'][1]
                pixelformat = conf['pixelformat']

                conf.pop('resolution')

                # set resolution
                subprocess.run([f'v4l2-ctl --set-fmt-video=width={width}',f'height={height}'],stdout=subprocess.DEVNULL, shell=True)
                # set pixelformat
                subprocess.call(['v4l2-ctl','--set-fmt-video',f'pixelformat={pixelformat}'],stdout=subprocess.DEVNULL, shell=True)
                for key, value in conf.items():
                    try:
                        subprocess.run([f'v4l2-ctl -d /dev/video0 -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
                    except KeyError:
                        print('Error trying to configure. Wrong Camera?')

                # Take picture
                pixelformat=pixelformat.lower()
                subprocess.call(['v4l2-ctl','--stream-mmap','--stream-count=1','--stream-skip=3','--stream-to='+'./'+STATIC_ROOT+'/best.'+pixelformat])


                fs = FileSystemStorage()
                photo = '.'+STATIC_ROOT+'/best.'+pixelformat

                with open(photo, 'rb') as f:
                    new_name = fs.save('best.'+pixelformat, File(f))
                    print(fs.url(new_name))
                    data = {
                        'url':request.META['HTTP_ORIGIN']+fs.url(new_name)
                    }

            print(form['FormatControlsForm'].errors)
            return JsonResponse(data)
