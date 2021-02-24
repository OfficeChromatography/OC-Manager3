#!/usr/bin/env python
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

from django.http import HttpResponse
from os import path
from .track_detection_core import calculate_tracks, image_to_sobel_signal, _normalize, _get_sobel_gray_img, _scan_x_axis, _extract_peaks
from .file_utils import load_rgb_img, create_dir, save_rgb_image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.signal import savgol_filter
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import io
from PIL import Image

# crops image to the selected bands start and front variables
def _crop_img(img, front, bands_start):
    h, _, _ = img.shape
    upper = h
    lower = 0
    if front:
        upper = int(front * h)
    if bands_start:
        lower = int(bands_start * h)
    return img[h - upper:h - lower]


class TrackDetection():
    """
    INTERFACE FOR HPTLC-TRACK PICKING

    TrackDetection(
      img_path='/path/to/chromatogram.jpg' 
      img=my_image_as_np_matrix, 
      number_of_tracks=20, 
      track_width=0.03, 
      scale_factor=0.4, 
      bands_start=0.1, 
      front=0.9) -> obj
    
    PARAMS
    ======

    Absolute or relative path to an image
    Hint: if img_path and img is set, img_path is loaded only
    img_path OR img: REQUIRED

    The number of visible tracks to extract
    number_of_tracks: optional

    Relative ratio between track width to image width 
    track_width: optional but recommended 

    Factor of image rescale. 
    # E.g. 1000px width with scale factor 0.5 will result in an 1000px width image    
    scale_factor: optional

    Relative ratio between band start to image height 
    bands_start: optional, 

    Relative ratio between frond to image height
    front=0.9) -> obj


    PROPERTIES
    =========

    tracks: array of hptlc_insight.track.Track Objects
    img : np array representing the cropped image
    img_original: np array representing the original sized image
    """

    def __init__(self,
                 img_path=None,
                 img=[],
                 number_of_tracks=None,
                 track_width=0.03,
                 #scale_factor=1,
                 bands_start=0,
                 front=1):
        if img_path:
            img = load_rgb_img(img_path)
        self._img = img
        self._height, self._width, _ = img.shape
        self._number_of_tracks = int(number_of_tracks)
        self._track_width = float(float(track_width) / float(self._width))
        #self._scale_factor = float(scale_factor)
        self._bands_start = float(float(bands_start) / float(self._height))
        self._front = float(float(front) / float(self._height))
        # would cause error, important for initial track detection run
        if self._front == 0:
            self._front = self._height
        if self._track_width == 0:
            self._track_width = 0.04

    @property
    def img_original(self):
        return self._img
    # imports immutable function calculating tracks from chromatogram image using sobel edges from track_detection_core
    
    @property
    def tracks(self):
        img = self.img
        return calculate_tracks(img, self._number_of_tracks, self._track_width)

    @property
    def img(self):
        return _crop_img(self._img, self._front, self._bands_start)

    def plot_tracks_on_chrom(self,
                             show_tracks=True,
                             show_signal=False,
                             show_crop=False,
                             show_track_numbers=False,
                             track_colour='#e6e6e6', 
                             signal_colour='#e6e6e6'):
        """plots found tracks on chromatogram image"""
        img = self.img
        img_to_show = self.img_original
        h, w, _ = self.img_original.shape
        start_px = self._bands_start * h
        front_px = self._front * h
        
        if show_crop:
            h, w, _ = self.img.shape
            start_px = self._bands_start
            front_px = h
            img_to_show = self.img

        tracks = self.tracks
        _, ax = plt.subplots(1)

        if show_signal:
            s = image_to_sobel_signal(img, int(self._track_width * w))
            s_norm = _normalize(s, h) # normalisation to 255 values
            plt.plot(s_norm, color=signal_colour, linewidth=2)

        if show_tracks:
            for t in tracks:
                width = t.width * w
                rect = patches.Rectangle((t.img_idx - width / 2, start_px),
                                         width,
                                         front_px - start_px,
                                         linewidth=2,
                                         edgecolor=track_colour,
                                         facecolor='none')
                ax.add_patch(rect)
          
        if show_track_numbers:
            offset = 5
            for idx, t in enumerate(tracks):
                idx += 1
                label = str(idx) if idx > 9 else " " + str(idx)
                ax.text(t.img_idx - 5, h + offset, label)

        ax.imshow(img_to_show, extent=[0, w, 0, h])



        plt.gca().set(xlabel="\nImage Width [px]", ylabel="Image Height [px]\n")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        plt.savefig(buf, transparent=True, bbox_inches="tight")  # ADDED SAVE IMAGE HERE
        plt.close()
        return buf

    def save_tracks_as_files(self, save_dir):
        """ 
        saves found tracks as jpg images in given directory 
        save_dir: str, absolute path to where images should bes saved
        """
        img = self.img
        create_dir(save_dir)
        for t in self.tracks:
            name = t.name
            track_img = t.to_image(img)
            save_name = path.join(save_dir, name + '.jpg')
            save_rgb_image(track_img, save_name)
