import os
import cv2


def load_rgb_img(img_path, size=1):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError('Could not load image from path ' + img_path)
    smaller = cv2.resize(img, (0, 0), fx=size, fy=size)
    return cv2.cvtColor(smaller, cv2.COLOR_BGR2RGB)


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def save_rgb_image(img, filename):
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr)
