#
#     hptlc-insight: automated hptlc analysis and evaluation
#     Copyright (C) 2015-2019 CMCC Foundation
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#from functools import lru_cache
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter, find_peaks, peak_prominences, peak_widths
from .track import Track

def _extract_prominences(signal, peaks):
    prominences, _, _ = peak_prominences(signal, peaks=peaks)
    filtered = []
    for idx in range(len(signal)):
        if idx in peaks:
            peak_idx = [i for i, p in enumerate(peaks) if idx == p][0]
            prom = prominences[peak_idx]
            filtered.append(prom)
        else:
            filtered.append(0)
    return filtered


def _scan_x_axis(img):
    """ 
    returns matrix m of shape h, w where each row represents the rgb channels and each col represents the summation of the images pixel values
    example: intensity signal of channel r: m[:, 0]
    """
    win_size = 5
    val_sum = np.sum(img, axis=0)
    return medfilt(val_sum / img.shape[1], win_size) # normalisation for channels available in image (RGB or grey)


def _normalize(image, height=255):
    return image * (height / image.max())


def _extract_peaks(signal):
    peaks, _ = find_peaks(signal)
    return _extract_prominences(signal, peaks)


def _img_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def _filter_edges(img, k, horizontal=1, vertical=0):
    sobel_filtered = cv2.Sobel(img, cv2.CV_64F, vertical, horizontal, ksize=k)
    return np.array(sobel_filtered)


def _subtract_signals(vertical, signal_hor):
    signal = signal_hor - vertical
    signal[signal < 0] = 0
    return signal


def _get_sobel_gray_img(img, k, horizontal=1, vertical=0):
    gray = _img_to_gray(img)
    sobeled = np.absolute(_filter_edges(gray, k, horizontal, vertical))
    return _normalize(sobeled).astype('uint8')


def _get_sobel_signal(img, k=31):
    """
    calculates signal on sobel edges

    img: numpy matrix representation of image
    k: sobel kernel size, must be odd
    """
    assert k % 2 == 1
    sobel_filtered_horizontal = _get_sobel_gray_img(img, k, 1, 0)
    sobel_filtered_vertical = _get_sobel_gray_img(img, k, 0, 1)
    signal_vert = _scan_x_axis(sobel_filtered_vertical)
    signal_hor = _scan_x_axis(sobel_filtered_horizontal)
    return _subtract_signals(signal_vert, signal_hor)


def _filter_no_of_tracks_by_intensity(tracks, no_of_tracks):
    tracks.sort(key=lambda t: t.intensity, reverse=True)
    sorted_tracks = tracks[:int(no_of_tracks)]
    sorted_tracks.sort(key=lambda t: t.img_idx)
    return sorted_tracks


def _get_tracks_from_signal(img, track_width, peak_signal):
    _, w, _ = img.shape
    tracks = []
    for idx, sig_tupel in enumerate(peak_signal):
        val = sig_tupel
        is_track = val > 0
        if is_track:
            track = Track(w, val, idx, track_width)
            tracks.append(track)
    return tracks



#@np_cache
def image_to_sobel_signal(img, window_size=25):
    """
    transforms img into a 1d signal depending on it's horizontal and vertical edges

    img: numpy matrix representation of image 
    window_size: width of the 2nd degree polynom approximation, must be odd

    returns 1d numpy array
    """
    pol = 2  # approximate unsmoothed signal to 2nd degree polynoms
    if window_size % 2 == 0:
        window_size = window_size - 1
    sobel_signal = _get_sobel_signal(img)
    smoothed_signal = savgol_filter(sobel_signal, window_size, pol)
    return smoothed_signal


#@np_cache
def create_signal_and_extract_peaks(img, width=0.02):
    """
    transforms img into a 1d array depending on it's horizontal and vertical edges

    img: numpy matrix representation of image 
    width: relative ratio between track width to image width, between 0 and 1  

    returns 1d numpy array
    """
    _, w, _ = img.shape
    width_px = int(float(width) * w)
    width_px_odd = width_px + 1 if width_px % 2 == 0 else width_px
    signal = image_to_sobel_signal(img, width_px_odd)
    return _extract_peaks(signal)


#@np_cache
def calculate_tracks(img, number_of_tracks, track_width):
    """
    immutable function calculating tracks from chromatogram image using sobel edges

    img: numpy matrix representation of image
    number_of_tracks: number of tracks on image
    track_width: relative ratio between track width to image width, between 0 and 1
    """
    peak_signal = create_signal_and_extract_peaks(img, track_width)
    tracks = _get_tracks_from_signal(img, track_width, peak_signal)
    return _filter_no_of_tracks_by_intensity(tracks, number_of_tracks)
