import cv2
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d


def _create_reference_list(reference):
    reference = str(reference).replace(' ', '')
    reference = reference.split(',')
    ref_list = []
    for entry in reference:
        if '-' in entry:
            ranges = entry.split('-')
            start, end = sorted(list(map(int, ranges)))
            for i in range(int(start) - 1, int(end)):
                ref_list.append(i)
        elif len(entry) > 0:
            ref_list.append(int(entry) - 1)
    return ref_list


def create_reference_dict(tracks, reference):
    reference_dir = {}
    for idx in range(len(tracks)):
        if idx in reference:
            reference_dir[str(idx + 1)] = 'red'
        else:
            reference_dir[str(idx + 1)] = 'black'
    return reference_dir


"""
def _load_signals(track_detection):
    tracks = track_detection.tracks
    track_rgbs = [t.to_rgb_densitogram(track_detection.img) for t in tracks]
    return track_rgbs
"""


def preprocess_chromatogram(img):
    return cv2.medianBlur(img, 15)


def get_tracks(td):
    img = td.img
    c = preprocess_chromatogram(img)
    tracks = td.tracks
    track_imgs = [t.to_image(c) for t in tracks]
    return np.array(track_imgs)


def normalize(signals):
    """normalize for each r, g, b channel"""
    # https://stackoverflow.com/questions/42460217/how-to-normalize-a-4d-numpy-array
    v_min = signals.min(axis=(0, 1), keepdims=True)
    v_max = signals.max(axis=(0, 1), keepdims=True)
    return (signals - v_min) / (v_max - v_min)


def norm_and_smooth(signals):
    scaled_signals = normalize(signals)
    return np.array([gaussian_filter1d(sig, sigma=3) for sig in scaled_signals])


def imgs_to_densitograms(track_imgs, c):
    signals = np.array([np.sum(img, axis=0)[:, c] for img in track_imgs])
    return norm_and_smooth(signals)


def create_combined_data(track_imgs):
    signal_r = np.array([np.sum(img, axis=0)[:, 0] for img in track_imgs])
    signal_g = np.array([np.sum(img, axis=0)[:, 1] for img in track_imgs])
    signal_b = np.array([np.sum(img, axis=0)[:, 2] for img in track_imgs])
    combined_channels = np.concatenate((signal_r, signal_g, signal_b), axis=1)
    return norm_and_smooth(combined_channels)
