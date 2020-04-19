from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm
from app.settings import STATIC_ROOT
from .models import PlatePhoto_Db
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import time
import subprocess


INITIALS = { 'brightness': 50,
            'contrast': 0,
            'saturation': 0,
            'red_balance': 1000,
            'blue_balance': 1000,
            'sharpness': 0,
            'auto_exposure': '0',
            'exposure_time_absolute': 1000,
            'iso_sensitivity': '0',
            'iso_sensitivity_auto': '0',
            'resolution':'1280x720',
            'framerate':'15.0',
            'pixelformat':'3'}

# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        form['form'] = ShootConfigurationForm(initial=INITIALS)
        return render(
                        request,
                        "capture.html",
                        form
                        )

    def post(self, request):
        form['form'] = ShootConfigurationForm(request.POST or None)
        if form['form'].is_valid():
            conf = form['form'].cleaned_data
            # devices = subprocess.check_output(['v4l2-ctl','--list-devices']).decode('utf-8').split('\n\t')
            # name = devices[0][0:].split(':')[0]
            # description = devices[0][0:].split(':')[1]
            # # .split('\n\t')
            # print(a)

            width = conf['resolution'][0]
            height = conf['resolution'][1]
            framerate = conf['framerate']
            pixelformat = conf['pixelformat']
            print(pixelformat)
            conf.pop('resolution')

            # set resolution
            subprocess.run(['v4l2-ctl',f'v4l2-ctl --set-fmt-video=width={width}',f'height={height}'],stdout=subprocess.DEVNULL, shell=True)
            # set framerate
            subprocess.call(['v4l2-ctl',f'--set-parm={framerate}'],stdout=subprocess.DEVNULL, shell=False)
            # start format
            subprocess.call(['v4l2-ctl','--set-fmt-video',f'pixelformat={pixelformat}'],stdout=subprocess.DEVNULL, shell=True)
            for key in conf:
                try:
                    subprocess.run([f'v4l2-ctl -d /dev/video0 -c {key}={str(conf[key])}'],stdout=subprocess.DEVNULL, shell=True)
                except KeyError:
                    print('Error trying to configure. Wrong Camera?')

            # Take picture
            subprocess.call('pwd',shell=True)
            subprocess.call(['v4l2-ctl','--stream-mmap','--stream-count=1','--stream-skip=3','--stream-to='+'./'+STATIC_ROOT+'/best.jpeg'])

            print(STATIC_ROOT+'/best.jpeg')
            # cap = cv2.VideoCapture(0)
            # cap.set(5,30)
            #
            # # cap.set(5,30)
            # # cap.set(9,0)
            # #
            # # # -64,64
            # # cap.set(10,conf['brightness'])
            # # # 0 a 95
            # # cap.set(11,conf['contrast'])
            # # # 0 a 100
            # # cap.set(12,conf['saturation'])
            # # # -2000 y 2000
            # # cap.set(13,conf['hue'])
            # # # 1 a 8
            # # cap.set(14,conf['gain'])
            # # #
            # # cap.set(15,conf['exposure'])
            #
            # ret, frame = cap.read()
            #
            # cv2.imwrite(filename=STATIC_ROOT+'best.jpg', img=frame)
            # cap.release()

            fs = FileSystemStorage()
            photo = '.'+STATIC_ROOT+'/best.jpeg'
            print(photo)
            with open(photo, 'rb') as f:
                name = fs.save('best.jpeg', File(f))
                print(fs.url(name))
                # foto = PlatePhoto_Db(name='foto1', photo=File(contents))
                data = {
                    'url':request.META['HTTP_ORIGIN']+fs.url(name)
                }

            # if request.FILES['GFile']:
            #     # Upload the Gcode file
            #     uploaded_file = request.FILES['GFile']
            #     if 'gcode' in uploaded_file.content_type:
            #         fs = FileSystemStorage()
            #         new_name = fs.save(uploaded_file.name, uploaded_file)
            #         with open(f'{fs.location}/{new_name}', 'r') as file:
            #             mylist = list(file)
            #             OC_LAB.send(mylist)
            #         return render(
            #                 request,
            #                 "./motorcontrol.html",
            #                 form)



            # UploadedFile.read('/best.jpg')
            # fs = FileSystemStorage()
            # fs.open('best.jpg')
            # fs.save('best.jpg')

                # new_name = fs.save(uploaded_file.name, uploaded_file)
                # with open(f'{fs.location}/{new_name}', 'r') as file:
                #     mylist = list(file)
                #     OC_LAB.send(mylist)
                # return render(
                #         request,
                #         "./motorcontrol.html",
                #         form)
        print(form['form'].errors)
        return render(
                        request,
                        "capture.html",
                        {**form, **data}
                        )
