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
from .track_detection import *
from .track import _rotate_track
from .track_detection_core import _scan_x_axis
import numpy as np
import io

def _get_intensity_on_rf(track, c_img, idx, width=1):
    t_img = track.to_image(c_img)
    offset = int(width / 2)
    offset = offset if offset > 0 else 1
    start = idx - offset
    end = idx + offset
    return np.sum(_scan_x_axis(t_img)[start:end])


def sort_tracks_by_intensity_at_rf(td, rf, width=1):
    """
    td:  hptlc_insight.track_detection.TrackDetection
    rf: floating point representing RF value
    width: window size of intensity calculation
    """
    tracks = td.tracks
    c_img = td.img
    h, _, _ = c_img.shape
    pick_in_px = int(h * rf)
    sorted_tracks = sorted(
        tracks,
        key=lambda t: _get_intensity_on_rf(t, c_img, pick_in_px, width),
        reverse=True)
    return sorted_tracks

"""
INTERFACE FOR PEAK SORTING

TrackSort(
    track_detection=td, 
    rf=0.2, 
    scan_width=10) -> obj

PARAMS
======
track_detection: object, required       object of class hptlc_insight.track_detection.TrackDetection
rf: float, required                     RF-Value of the sorted peak
scan_width: int, optional               pixel width on which the intensity calculation is based on
    
PROPERTIES
=========
rf : rf value
scan_width:                             pixel width on which the intensity calculation is based on
"""

class TrackSort():

    def __init__(self, track_detection, rf, scan_width=1):
        self._td = track_detection
        self.rf = float(rf)
        self.scan_width = int(scan_width)   # scan width defines the width of relevant pixel values in y direction in range: rf - (width/2) to rf + (width/2)

    #helper function for plotting multiple tracks
    def plot_multiple_tracks(tracks, track_imgs, rows, cols, rf):
        all_track_idxs = []
        tracksort_buf = io.BytesIO()
        for track in tracks:
            all_track_idxs.append(track.img_idx)
        all_track_idxs = sorted(all_track_idxs)
        h, w, c = np.array(track_imgs[0]).shape
        rf_to_px = int(h * rf)
        fig = plt.figure(figsize=(20,8))
        
        for idx in range(1, rows * cols +1 ):        
            fig.add_subplot(rows, cols, idx, frameon=True)
            plt.title(str(all_track_idxs.index(tracks[idx-1].img_idx)+1))
            plt.axhline(y=rf_to_px, color = 'red')
            plt.imshow(track_imgs[idx-1], extent=[0, w, 0, h])
            if not idx == 1:
                plt.axis('off')
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        #fig.text(0.5, 0.3, 'Track Width as Specified by the User [px]', ha='center')
        plt.savefig(tracksort_buf, transparent=True, bbox_inches="tight")
        tracksort_buf.seek(0)
        plt.close()
        return tracksort_buf

    # returns a sorted list (descending) of hptlc_insight.track.Track objects 
    def sort_tracks_by_intensity(self):
        return sort_tracks_by_intensity_at_rf(self._td, 
                                              self.rf,
                                              self.scan_width)
    
    # sorts tracks using TrackSort and plot each image with a red horizontal line
    def sort_tracks_by_rf(self):
        sorted_tracks = self.sort_tracks_by_intensity()
        track_imgs = [t.to_image(self._td.img, False) for t in sorted_tracks]
        return TrackSort.plot_multiple_tracks(sorted_tracks, track_imgs, 1, len(track_imgs), self.rf)



