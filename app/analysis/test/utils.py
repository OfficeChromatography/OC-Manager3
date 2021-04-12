import glob
import os

IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/test_image.png'

def remove_files_from_local(path):
    for i in glob.glob(path):
        os.remove(i)
