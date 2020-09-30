from app.settings import STATIC_ROOT, MEDIA_ROOT
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm, AligmentConfigurationForm, LedsControlsForm
from .models import Images_Db

from django.core.files import File
from PIL import Image
import PIL.ExifTags
from PIL.ExifTags import TAGS
import time
import subprocess
import os
from datetime import datetime

import cv2
import numpy as np

from connection.forms import OC_LAB

def basic_conf():
    basic_conf = {'brightness': 50,
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
                'scene_mode':0,

                'uv365_power':0,
                'uv278_power':0,
                'red':100,
                'blue':100,
                'green':100,
                'brightness_rgb':100,
                }
    return basic_conf

def take_photo(request):
    format_config = ShootConfigurationForm(request.POST or None)
    camera_config = CameraControlsForm(request.POST or None)
    user_config = UserControlsForm(request.POST or None)
    led_config = LedsControlsForm(request.POST or None)

    data={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
    if camera_config.is_valid():
        for key, value in camera_config.cleaned_data.items():
            subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
    else:
        print(camera_config.errors)

    if user_config.is_valid():
        for key, value in user_config.cleaned_data.items():
            subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
    else:
        print(user_config.errors)

    if led_config.is_valid():
        led_control(led_config.cleaned_data)
        time.sleep(1)
    else:
        print(led_config.errors)

    if format_config.is_valid():
        conf = format_config.cleaned_data
#         print("ESta es la conf/n"conf)
        width = conf['resolution'][0]
        height = conf['resolution'][1]
        pixelformat = conf['pixelformat']

        conf.pop('resolution')

        # set resolution
        subprocess.run([f'v4l2-ctl --set-fmt-video=width={width},height={height}'],stdout=subprocess.DEVNULL,shell=True)

        # set format
        subprocess.call(['v4l2-ctl','--set-fmt-video',f'pixelformat={pixelformat}'],
                        stdout=subprocess.DEVNULL,
                        shell=True)

    for key, value in conf.items():
        try:
            subprocess.run([f'v4l2-ctl -d /dev/video0 -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
        except KeyError:
            print('Error trying to configure. Wrong Camera?')

    photo_path = shoot(pixelformat)

    # Turn off leds
    led_control()

    return photo_path

def shoot(format):
    # Take picture
    format=format.lower()
    name = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    photo_path='.'+MEDIA_ROOT+'/images/'+name+'.'+format
    subprocess.call(['v4l2-ctl','--stream-mmap','--stream-count=1','--stream-skip=3','--stream-to='+photo_path])
    return photo_path

def save_photo_db(path_to_photo,user):
    with open(path_to_photo,'rb') as f:
        image = Images_Db()
        image.photo = File(f)
        image.save()
        image.filename = image.file_name()
        image.uploader = user
        image.save()
        return image

def led_control(led_config=None):
# Power from: 0~255
# Wavelength: 255,365,visible
    if led_config != None:
        visible_ligth = "G93"
        print(led_config)
        for key, value in led_config.items():
            if key == 'uv365_power':
                OC_LAB.send_now(f'M42 P4 S{value}')
            if key == 'uv278_power':
                OC_LAB.send_now(f'M42 P5 S{value}')
            if key == 'red':
                visible_ligth += f'R{value}'
            if key == 'green':
                visible_ligth += f'G{value}'
            if key == 'blue':
                visible_ligth += f'B{value}'
            if key == 'brightness_rgb':
                visible_ligth += f'I{value}'
        OC_LAB.send_now(visible_ligth)
    else:
        OC_LAB.send_now(f'M42 P4 S0')
        OC_LAB.send_now(f'M42 P5 S0')
        OC_LAB.send_now('G93R0B0G0I0')



def get_metadata(image_in_Db):
#     path = os.path.join('./', str(image_in_Db.photo))
#     print(path)
    img = Image.open("./media/images/best1.jpeg")
    exifdata = img.getexif()
    print(exifdata)
    dic={}
    img_data = ""
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        img_data += f"{tag}: {data}\n"
        dic[tag]=str(data)
    return filter_data(dic)



def filter_data(data):
    values = ["BrightnessValue","ImageWidth","ImageLength","Model","ExposureTime",
    "XResolution","YResolution","ExposureProgram","ISOSpeedRatings",
    "ResolutionUnit","ExifOffset","ExposureMode","WhiteBalance"]
    return dict(filter(lambda x: x[0] in values, data.items()))

def manipulate(path):
# Corrects the images bending, product of using a fisheye lens
# Hardcoded values for HQPicamera

    mtx=np.array([[2009.9439533949294, 0.0, 1099.0825337234287], [0.0, 1981.8528472526064, 719.3003764740773], [0.0, 0.0, 1.0]])
    dist=np.array([[-0.4452686852311272, 0.16206091566188818, 0.0018999163210796088, -0.002555211352544398, -0.007024199063685075]])

    img = cv2.imread(path)

    h,w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    new_path = f'{os.path.splitext(path)[0]}_corrected{os.path.splitext(path)[1]}'
    cv2.imwrite(new_path,dst)

    return new_path

