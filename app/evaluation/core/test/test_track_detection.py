import pytest
from ..hptlc_insight.track_detection import TrackDetection
from ..hptlc_insight.file_utils import save_rgb_image
import io
import cv2
import numpy as np
from PIL import Image

testdata_track_detection = {"img_path":'./test_image.png',
                            "number_of_tracks":20,
                            "track_width":19,
                            "bands_start":12,
                            "front":164
}

testdata_plot_track_on_chromatograms = [(True, False, False, False, '#e6e6e6', '#e6e6e6',)]


def buffer_to_image(buffer):
    return cv2.imdecode(np.frombuffer(buffer.getbuffer(), np.uint8), -1)


@pytest.fixture
def track_detection():
    return TrackDetection(img_path=testdata_track_detection["img_path"],
                          number_of_tracks=testdata_track_detection["number_of_tracks"],
                          track_width=testdata_track_detection["track_width"],
                          bands_start=testdata_track_detection["bands_start"],
                          front=testdata_track_detection["front"])


def test_creating_track_detection_instance(track_detection) -> None:
    assert isinstance(track_detection, TrackDetection)


@pytest.mark.parametrize("show_track_numbers,show_crop,show_signal,show_tracks,track_colour,signal_colour",
                         testdata_plot_track_on_chromatograms)
def test_plot_tracks_on_chromatograms(track_detection,
                                      show_track_numbers,
                                      show_crop,
                                      show_signal,
                                      show_tracks,
                                      track_colour,
                                      signal_colour):
    buf = track_detection.plot_tracks_on_chrom(show_tracks=show_track_numbers,
                                               show_signal=show_crop,
                                               show_crop=show_signal,
                                               show_track_numbers=show_tracks,
                                               track_colour=track_colour,
                                               signal_colour=signal_colour)
    assert isinstance(buf, io.BytesIO)


def test_save_tracks_as_list_of_buffer(track_detection):
    list_of_buffers = track_detection.save_tracks_as_list_of_buffer()
    assert len(list_of_buffers) == 20
    for index,value in enumerate(list_of_buffers):
        assert len(value.getvalue()) >= 100

