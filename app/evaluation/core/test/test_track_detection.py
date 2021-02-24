import pytest
from ..hptlc_insight.track_detection import TrackDetection
import io
from PIL import Image

testdata_plot_track_on_chromatograms = [(True, False, False, False, '#e6e6e6', '#e6e6e6',)]


@pytest.fixture
def track_detection():
    return TrackDetection(img_path='./test_image.png',
                          number_of_tracks=20,
                          track_width=19,
                          bands_start=12,
                          front=164)


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
