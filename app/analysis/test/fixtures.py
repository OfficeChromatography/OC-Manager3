import pytest
import os
from django.contrib.auth.models import User
from app.settings import MEDIA_ROOT
from django.core.files import File
from ..models import Images_Db, TrackDetection_Db, PlotOnChromatograms_Db, TrackInspection_Db, TrackSort_Db, PCAAnalysis_Db, Heatmap_Db, HCAAnalysis_Db

USERNAME = "root"
PASSWORD = "123456"

TEST_IMAGE_PATH = os.path.join(MEDIA_ROOT, "test.png")

@pytest.fixture
def media_root():
    yield MEDIA_ROOT

@pytest.fixture
def user():
    return User.objects.create_user(username=USERNAME, password=PASSWORD)


@pytest.fixture
def client(client):
    client.login(username=USERNAME, password=PASSWORD)
    return client


@pytest.fixture
def image_object(user):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'image': File(image),
            'filename': 'test',
            'uploader': user,
        }
        object = Images_Db.objects.create(**data)
        yield object
    os.remove(object.image.path)


@pytest.fixture
def track_detection_object(image_object):
    data = {
            'image': image_object,
            'number_of_tracks': 20,
            'track_width': 19,
            'bands_start': 12,
            'front': 164,
        }
    object = TrackDetection_Db.objects.create(**data)
    yield object

@pytest.fixture
def plot_on_chromatogram_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'image': File(image),
            'show_tracks': True,
            'show_signal': True,
            'show_crop': True,
            'show_track_numbers': True,
            'track_colour': '#000000',
            'signal_colour': '#000000',
        }
        object = PlotOnChromatograms_Db.objects.create(**data)
        yield object
    os.remove(object.image.path)

@pytest.fixture
def track_inspection_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'track_number': 10,
            'track_image': File(image),
            'rgb_densitogram': File(image)
        }
        object = TrackInspection_Db.objects.create(**data)
        yield object
    os.remove(object.track_image.path)
    os.remove(object.rgb_densitogram.path)

@pytest.fixture
def track_sort_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'rf': 0.7,
            'sorted_image': File(image)
        }
        object = TrackSort_Db.objects.create(**data)
        yield object
    os.remove(object.sorted_image.path)

@pytest.fixture
def pca_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'reference': '1-5',
            'explained_variance': File(image),
            'pca': File(image),
        }
        object = PCAAnalysis_Db.objects.create(**data)
        yield object
    os.remove(object.explained_variance.path)
    os.remove(object.pca.path)

@pytest.fixture
def heatmap_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'reference': '1-5',
            'heatmap': File(image),
        }
        object = Heatmap_Db.objects.create(**data)
        yield object
    os.remove(object.heatmap.path)

@pytest.fixture
def hca_object(track_detection_object):
    with open(TEST_IMAGE_PATH, 'rb') as image:
        data = {
            'track_detection': track_detection_object,
            'reference': '1-5',
            'hca_tracks': File(image),
            'hca': File(image),
            'num_clusters': 5,
        }
        object = HCAAnalysis_Db.objects.create(**data)
        yield object
    os.remove(object.hca_tracks.path)
    os.remove(object.hca.path)

