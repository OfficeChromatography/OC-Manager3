from datetime import datetime
from app.settings import STATIC_ROOT, MEDIA_ROOT
import subprocess
import re
import glob
import pytz         #Import Timezone Library
from connection.forms import OC_LAB

tz = pytz.timezone('Europe/Berlin') #Setting Timezone for Berlin


class Camera:
    @classmethod
    def list_cameras(cls):
        # Returns a list with all the video* devices
        return glob.glob('/dev/video*')

    def __init__(self):
        pass
        # self.set_camera(camera_device)

    def set_camera(self, camera_device):
        self.camera_device = camera_device

    def shoot(self, format):
        # Take picture
        format = format.lower()
        name = self.create_time_stamp()
        photo_path = MEDIA_ROOT + '/images/' + name + '.' + format
        process = subprocess.run(
            ['v4l2-ctl', '--stream-mmap', '--stream-count=1', '--stream-skip=3', '--stream-to=' + photo_path],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        if process.returncode == 0:
            print('The photo was taken')
            return photo_path
        return None

    def create_time_stamp(self):
        return datetime.now(tz).strftime("%Y.%m.%d-%H.%M.%S")

    def set_camera_property(self, property, value):
        # Sets the property value
        process = subprocess.run([f'v4l2-ctl', '-c', f'{property}={value}'], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        if process.returncode == 0:
            print(f'{property} set to: {value}')
        else:
            print(f'Error setting {property}')

    def set_resolution(self, width, height):
        process = subprocess.run([f'v4l2-ctl --set-fmt-video=width={width},height={height}'], shell=True)
        if process.returncode == 0:
            print(f'Resolution set to:{width}x{height}')
        else:
            print(f'Error setting resolution to:{width}x{height}')

    def get_camera_property_value(self, property):
        # Returns a string with the value of the property
        process = subprocess.run([f'v4l2-ctl', '-C', f'{property}'], stdout=subprocess.PIPE, universal_newlines=True)
        if process.returncode == 0:
            print(process.stdout)
            return re.findall(r"(\d+)", process.stdout)[0]
        else:
            print(f"Error trying to query the {property} property")

    def get_all_camera_properties(self):
        # Returns a String with all the Camera Configurations and values
        process = subprocess.run(['v4l2-ctl', '-l'], stdout=subprocess.PIPE, universal_newlines=True)
        if process.returncode == 0:
            print(process.stdout)
        return process.stdout


class UvLed:
    def __init__(self, pin):
        self.pin = pin

    def set_power(self, power):
        OC_LAB.send_now(f'M42 P{self.pin} S{power}')


class VisibleLed:
    def __init__(self):
        pass

    def set_rgb(self, red_power, blue_power, green_power):
        OC_LAB.send_now(f'G93R{red_power}B{blue_power}G{green_power}I100')
