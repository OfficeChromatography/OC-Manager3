from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm
import cv2
from app.settings import STATIC_ROOT
from .models import PlatePhoto_Db
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import time
import subprocess

cam_props = {'brightness': 128, 'contrast': 128, 'saturation': 180,
             'gain': 0, 'sharpness': 128, 'exposure_auto': 1,
             'exposure_absolute': 150, 'exposure_auto_priority': 0,
             'focus_auto': 0, 'focus_absolute': 30, 'zoom_absolute': 250,
             'white_balance_temperature_auto': 0, 'white_balance_temperature': 3300}
# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        form['form'] = ShootConfigurationForm()
        return render(
                        request,
                        "capture.html",
                        form
                        )

    def post(self, request):
        form['form'] = ShootConfigurationForm(request.POST or None)
        if form['form'].is_valid():
            conf = form['form'].cleaned_data
            print(conf)

            subprocess.call(['v4l2-ctl --list-devices'])
            for key in conf:
                subprocess.call([f'v4l2-ctl -d /dev/video0 -c {key}={str(cam_props[key])}'],shell=True)
            cap = cv2.VideoCapture(0)

            # 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
            # 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
            # 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
            # 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
            # 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
            # 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
            # cap.set(5,30)
            # cap.set(9,0)
            #
            # # -64,64
            # cap.set(10,conf['brightness'])
            # # 0 a 95
            # cap.set(11,conf['contrast'])
            # # 0 a 100
            # cap.set(12,conf['saturation'])
            # # -2000 y 2000
            # cap.set(13,conf['hue'])
            # # 1 a 8
            # cap.set(14,conf['gain'])
            # #
            # cap.set(15,conf['exposure'])

            ret, frame = cap.read()

            cv2.imwrite(filename=STATIC_ROOT+'best.jpg', img=frame)
            cap.release()

            fs = FileSystemStorage()
            photo = STATIC_ROOT+'best.jpg'
            with open(photo, 'rb') as f:
                name = fs.save('best.jpg', File(f))
                print(fs.url(name))
                # foto = PlatePhoto_Db(name='foto1', photo=File(contents))
                data = {
                    'url':'http://127.0.0.1:8000'+fs.url(name)
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
