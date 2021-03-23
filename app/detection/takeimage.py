from app.settings import STATIC_ROOT, MEDIA_ROOT
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm, AligmentConfigurationForm, LedsControlsForm
from .models import Images_Db

from finecontrol.forms import Method_Form
from finecontrol.models import Method_Db

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

from .Camera import *

def basic_conf():
    basic_conf = {'brightness': 50,
                  'contrast': 0,
                  'saturation': 0,
                  'red_balance': 1000,
                  'blue_balance': 1000,
                  'sharpness': 0,
                  'color_effects': 0,
                  'power_line_frequency': 1,
                  'horizontal_flip': 0,
                  'vertical_flip': 0,
                  'rotate': 0,
                  'color_effects_cbcr': 32896,

                  'resolution': '2028x1520',
                  'pixelformat': 3,

                  'auto_exposure': 1,
                  'exposure_dynamic_framerate': 0,
                  'auto_exposure_bias': 12,
                  'exposure_time_absolute': 1000,
                  'exposure_metering_mode': 0,
                  'white_balance_auto_preset': 1,
                  'image_stabilization': 0,
                  'iso_sensitivity_auto': 1,
                  'iso_sensitivity': 0,
                  'scene_mode': 0,

                  'uv365_power': 0,
                  'uv255_power': 0,
                  'red': 0,
                  'blue': 0,
                  'green': 0,
                  }
    return basic_conf

def get_metadata(image_in_Db):
    #     path = os.path.join('./', str(image_in_Db.photo))
    #     print(path)
    img = Image.open("./media/images/best1.jpeg")
    exifdata = img.getexif()
    print(exifdata)
    dic = {}
    img_data = ""
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        img_data += f"{tag}: {data}\n"
        dic[tag] = str(data)
    print(filter_data(dic))
    return filter_data(dic)


def filter_data(data):
    values = ["BrightnessValue", "ImageWidth", "ImageLength", "Model", "ExposureTime",
              "XResolution", "YResolution", "ExposureProgram", "ISOSpeedRatings",
              "ResolutionUnit", "ExifOffset", "ExposureMode", "WhiteBalance"]
    return dict(filter(lambda x: x[0] in values, data.items()))


'''New Code'''


class PhotoShootManager:

    def __init__(self, request):
        print(request)
        self.camera = Camera()
        self.nm_255 = UvLed(5)
        self.nm_365 = UvLed(4)
        self.visible_leds = VisibleLed()

        self.user = request.user
        self.camera_config_form = CameraControlsForm(request.POST or None)
        self.user_config_form = UserControlsForm(request.POST or None)
        self.format_config_form = ShootConfigurationForm(request.POST or None)
        self.led_config_form = LedsControlsForm(request.POST or None)
        #self.method_form = Method_Form(request.POST or None)

        self.id = request.POST.get("id")
        print(request.POST)
        self.path_photo = None

    def are_shoot_options_correct(self):
        # Checks the Camera_config, user_Config, the format_config
        # Returns the instance of filled forms
        if self.camera_config_form.is_valid() and \
                self.user_config_form.is_valid() and \
                self.format_config_form.is_valid() and \
                self.led_config_form.is_valid():
            return True
        else:
            print(self.camera_config_form.errors + '\n' +
                  self.user_config_form.errors + '\n' +
                  self.format_config_form.errors + '\n' +
                  self.led_config_form.errors)
            return False

    def set_camera_configurations(self):
        # Set the camera Configurations
        for key, value in self.camera_config_form.cleaned_data.items():
            self.camera.set_camera_property(key, value)
        for key, value in self.user_config_form.cleaned_data.items():
            self.camera.set_camera_property(key, value)

        width = self.format_config_form.cleaned_data['resolution'][0]
        height = self.format_config_form.cleaned_data['resolution'][1]
        self.camera.set_resolution(width, height)

    def shoot(self):
        self.nm_255.set_power(self.led_config_form.cleaned_data['uv255_power'])
        self.nm_365.set_power(self.led_config_form.cleaned_data['uv365_power'])
        self.visible_leds.set_rgb(
            self.led_config_form.cleaned_data['red'],
            self.led_config_form.cleaned_data['green'],
            self.led_config_form.cleaned_data['blue'],
        )

        file_format = self.format_config_form.cleaned_data['pixelformat']
        self.path_photo = self.camera.shoot(file_format)

        self.nm_255.set_power(0)
        self.nm_365.set_power(0)
        self.visible_leds.set_rgb(0, 0, 0)

    def save_photo_in_db(self):
        with open(self.path_photo, 'rb') as f:
            image = Images_Db()
            image.image.save(os.path.basename(self.path_photo), File(f))
            image.save()
            image.filename = image.file_name()
            image.uploader = self.user
            image.user_conf = self.user_config_form.save()
            image.leds_conf = self.led_config_form.save()
            image.camera_conf = self.camera_config_form.save()
            image.method = Method_Db.objects.get(pk=self.id)
            
            #print(self.camera_config_form,self.method_form)
            image.save()
            return image

    def photo_correction(self):
        # Corrects the images bending, product of using a fisheye lens
        # Hardcoded values for HQPicamera
        fixed_image = FixDistortionImage(self.path_photo)
        self.path_photo = fixed_image.path_photo


class FixDistortionImage:

    def __init__(self, path):
        self.path_photo = path
        self.img = cv2.imread(self.path_photo)

        self.correction_mtx = np.array([[1967.921637060819, 0.0, 980.07213571975], [0.0, 1964.823317953312, 741.073015742526], [0.0, 0.0, 1.0]])

        self.correction_dist = np.array([[-0.4778321949564693, 0.2886513041769561, 0.0016895448886501186, 0.0047619737564622905, -0.12895314122999252]])


        self.rotation_angle = 0.5

        # Undistort the image
        self.undistort()

    def undistort(self):
        # Using the fixed values mtx and dist, it straighten the image
        # and also cut the black borders
        h, w = self.img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.correction_mtx,
                                                          self.correction_dist,
                                                          (w, h),
                                                          1,
                                                          (w, h))
        # undistort
        dst = cv2.undistort(self.img,
                                 self.correction_mtx,
                                 self.correction_dist,
                                 None,
                                 newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        self.path_photo = f'{os.path.splitext(self.path_photo)[0]}_corrected{os.path.splitext(self.path_photo)[1]}'

        new_image = self.rotate_image(dst, self.rotation_angle)
        crop_img = new_image[40:1190, 310:1490]

        cv2.imwrite(self.path_photo, new_image)

    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
