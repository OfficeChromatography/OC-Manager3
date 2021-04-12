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

import numpy as np


def _rotate_track(track_img):
    return np.array(list(list(x)[::-1] for x in zip(*track_img)))


class Track():
    """
    Representation of a hptlc track
    All properties within this class are transformed into relative positions.


    Track(800, 42, 400, 47) -> obj

    PARAMS
    ======

    image_width: int, width of the chromatogram's image in px
    intensity: number, intensity in AU representing the track's sharpness
    img_idx: int, index on images x axis where the peak was found
    width: int, track's widht in px

    """

    def __init__(self, image_width, intensity, img_idx, width):
        self.width = float(width)
        self.img_idx = int(img_idx)
        self.intensity = float(intensity)
        self._set_track_start(int(image_width))
        self._set_track_end(int(image_width))
        self.relative_pos = int(img_idx) / int(image_width)

    def _set_track_start(self, image_width):
        side_width = int(float(self.width) * image_width / 2)
        start_left = self.img_idx - side_width
        if start_left < 0:
            start_left = 0
        self.track_start = start_left

    def _set_track_end(self, image_width):
        end_right = int(self.track_start + (self.width * image_width))
        if end_right > image_width:
            end_right = image_width
        self.track_end = end_right

    @property
    def name(self):
        return "pos_" + str(self.track_start) + "-" + str(
            self.track_end) + "_int_" + str(self.intensity)

    def to_image(self, img: np.ndarray, is_rotated=True):
        """
        extracts image containing this track
        @param img numpy matrix format
        """
        ret_img = []
        if self.width == 1:
            # calculate index for only one pixel
            idx = self.track_start - 1 if self.track_start > 0 else 0
            ret_img = img[:, [idx]]
        else:
            ret_img = img[:, self.track_start:self.track_end]
        if is_rotated: # before rotation of vertical track: RGB values per y-coordinate of track (length)
            ret_img = _rotate_track(ret_img)   # after rotation of vertical (now horizontal) track: RGB values for all x-coordinates of the track (width)

        return ret_img

    def to_rgb_densitogram(self, img):
        track_img = self.to_image(img)
        s = np.sum(track_img, axis=0)
        return np.transpose(np.array(s))

    def __str__(self):
        return 'width: ' + str(self.width) + \
            ' img_idx: ' + str(self.img_idx) + \
            ' intensity: ' + str(self.intensity) + \
            ' track_start: ' + str(self.track_start) + \
            ' track_end: ' + str(self.track_end) + \
            ' relative_pos: ' + str(self.relative_pos)
