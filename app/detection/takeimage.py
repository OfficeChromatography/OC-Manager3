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

                'resolution':'2028x1520',
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
                'uv255_power':0,
                'red':0,
                'blue':0,
                'green':0,
                }
    return basic_conf

def set_user_conf(request):
    user_config = UserControlsForm(request.POST or None)
    if user_config.is_valid():
        object_in_db = user_config.save()
        for key, value in user_config.cleaned_data.items():
            subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
    else:
        print(user_config.errors)
    return object_in_db

def set_camera_conf(request):
    camera_config = CameraControlsForm(request.POST or None)
    if camera_config.is_valid():
        object_in_db = camera_config.save()
        for key, value in camera_config.cleaned_data.items():
            subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
    else:
        print(camera_config.errors)
    return object_in_db

def set_LEDs_conf(request):
    led_config = LedsControlsForm(request.POST or None)
    if led_config.is_valid():
        object_in_db = led_config.save()
        led_control(led_config.cleaned_data)
        time.sleep(1)
    else:
        print(led_config.errors)
    return object_in_db

def set_format_conf(request):
    format_config = ShootConfigurationForm(request.POST or None)
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

    return pixelformat

def shoot(format):
    # Take picture
    format=format.lower()
    name = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    photo_path=MEDIA_ROOT+'/images/'+name+'.'+format
    subprocess.call(['v4l2-ctl','--stream-mmap','--stream-count=1','--stream-skip=3','--stream-to='+photo_path])
    return photo_path

def take_photo(request):
    # Apply config to the camera.
    camera_conf = set_camera_conf(request)
    user_conf = set_user_conf(request)
    leds_conf = set_LEDs_conf(request)
    pixelformat = set_format_conf(request)

    # Shoot the camera
    photo_path = shoot(pixelformat)

    # It Turn off the all the LEDs after image was taken
    led_control()

    photo_path = manipulate(photo_path)

    image = save_photo_db(photo_path,request.user,camera_conf, user_conf, leds_conf)

    return image



def save_photo_db(path_to_photo,user,camera_conf, user_conf, leds_conf):
    with open(path_to_photo,'rb') as f:
        image = Images_Db()
        image.photo.save(os.path.basename(path_to_photo), File(f))
        image.save()
        image.filename = image.file_name()
        image.uploader = user
        image.user_conf = user_conf
        image.leds_conf = leds_conf
        image.camera_conf = camera_conf
        image.save()
        return image

def led_control(led_config=None):
# Power from: 0~255
# Wavelength: 255,365,visible
    if led_config != None:
        visible_ligth = "G93"
        for key, value in led_config.items():
            if key == 'uv365_power':
                OC_LAB.send_now(f'M42 P4 S{value}')
            if key == 'uv255_power':
                OC_LAB.send_now(f'M42 P5 S{value}')
            if key == 'red':
                visible_ligth += f'R{value}'
            if key == 'green':
                visible_ligth += f'G{value}'
            if key == 'blue':
                visible_ligth += f'B{value}'
        visible_ligth += f'I{0}'
        print(visible_ligth)
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

    mtx=np.array([[1991.3292233320853, 0.0, 992.1223085915041], [0.0, 2001.2864268641247, 786.5630450127695], [0.0, 0.0, 1.0]])
    dist=np.array([[-0.46707485052454495, 0.23625331260723254, -0.002908698179874141, -0.00012139744702328517, -0.061287983893568314]])

    img = cv2.imread(path)

    h,w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    new_path = f'{os.path.splitext(path)[0]}_corrected{os.path.splitext(path)[1]}'

    new_image = rotate_image(dst,1.2)

    crop_img = new_image[100:500, 300:900]

    cv2.imwrite(new_path, crop_img)
    return new_path

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result