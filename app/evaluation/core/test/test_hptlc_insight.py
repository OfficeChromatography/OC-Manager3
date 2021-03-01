import pytest

from ..hptlc_insight.track_detection import TrackDetection
from ..hptlc_insight.track_inspection import TrackInspection
from ..hptlc_insight.track_sort import TrackSort
from ..hptlc_insight.pca_analysis import PCA_Analysis
from ..hptlc_insight.heatmap import Heatmap
from ..hptlc_insight.hca_analysis import HCA_Analysis

from ..hptlc_insight.file_utils import save_rgb_image
import io, os, cv2
import numpy as np
from PIL import Image

testdata_track_detection = {"img_path": './test_image.png',
                            "number_of_tracks": 20,
                            "track_width": 19,
                            "bands_start": 12,
                            "front": 164
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


######################################  Test TrackDetection    ######################################

def test_creating_track_detection_instance(track_detection) -> None:
    assert isinstance(track_detection, TrackDetection)


@pytest.mark.parametrize("show_track_numbers,show_crop,show_signal,show_tracks,track_colour,signal_colour",
                         testdata_plot_track_on_chromatograms)
def test_plot_tracks_on_chromatograms_and_save_in_file(track_detection,
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
    image = buffer_to_image(buf)
    # Save it in a file
    cv2.imwrite('./img.png', image)
    assert isinstance(buf, io.BytesIO)
    assert os.path.isfile('./img.png')

    os.remove("./img.png")


def test_save_tracks_as_list_of_buffer_and_save_in_file(track_detection):
    list_of_buffers = track_detection.save_tracks_as_list_of_buffer()
    for index, value in enumerate(list_of_buffers):
        img = buffer_to_image(value)
        filename = f'./track_img{index}.png'
        cv2.imwrite(filename, img)

        assert isinstance(value, io.BytesIO)
        assert os.path.isfile(filename)
        os.remove(filename)


######################################  Test TrackInspection    ######################################
def test_track_inspection(track_detection):
    for i in range(0, 20):
        track, densitogram = TrackInspection.show_densitogram_and_signal(track_detection, i)
        img_track = buffer_to_image(track)
        img_densitogram = buffer_to_image(densitogram)

        cv2.imwrite("img_track.png", img_track)
        cv2.imwrite("img_densitogram.png", img_densitogram)

        assert os.path.isfile('img_track.png')
        assert os.path.isfile('img_densitogram.png')

        os.remove('img_track.png')
        os.remove('img_densitogram.png')


######################################  Test TrackSort      ######################################
def test_track_sort(track_detection):
    rf_value = 0.7
    track_sort = TrackSort(track_detection, rf_value)
    buf = track_sort.sort_tracks_by_rf(float(rf_value))
    img = buffer_to_image(buf)
    cv2.imwrite("test_sorted.png", img)
    assert os.path.isfile('test_sorted.png')

    os.remove('test_sorted.png')


######################################  Test PCA_Analysis      ######################################
def test_pca_analysis(track_detection):
    reference = "1-5"
    pca = PCA_Analysis(track_detection, reference)
    buf_explained_variance = pca.plot_explained_variance()
    buf_pca = pca.plot_pca()
    img_explained_variance = buffer_to_image(buf_explained_variance)
    img_pca = buffer_to_image(buf_pca)
    cv2.imwrite("test_explained_PCA.png", img_explained_variance)
    cv2.imwrite("test_PCA.png", img_pca)

    assert os.path.isfile('test_explained_PCA.png')
    assert os.path.isfile('test_PCA.png')

    os.remove('test_explained_PCA.png')
    os.remove('test_PCA.png')


######################################  Test Heatmap        ######################################
def test_heatmap(track_detection):
    reference = "1-5"
    heatmap = Heatmap(track_detection, reference)
    heatmap_buf = heatmap.plot_heatmaps()
    heatmap_img = buffer_to_image(heatmap_buf)
    cv2.imwrite("heatmap.png", heatmap_img)

    assert os.path.isfile('heatmap.png')

    os.remove('heatmap.png')

######################################  Test HCA_Analysis       ######################################
def test_hca_analysis(track_detection):
    reference = "1"
    num_tracks = 20
    hca = HCA_Analysis(track_detection, reference, num_tracks)
    hca_buf, hca_tracks_buf = hca.plot_dendrogram()
    hca_img = buffer_to_image(hca_buf)
    hca_tracks_img = buffer_to_image(hca_tracks_buf)

    cv2.imwrite("hca_img.png", hca_img)
    cv2.imwrite("hca_tracks_img.png", hca_tracks_img)
    assert os.path.isfile('hca_img.png')
    assert os.path.isfile('hca_tracks_img.png')

    os.remove('hca_img.png')
    os.remove('hca_tracks_img.png')

