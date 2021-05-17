import pytest
from django.urls import reverse
from app.settings import MEDIA_ROOT
from .utils import remove_files_from_local
import json
import os.path

pytestmark = pytest.mark.django_db


class TestChromatogramPlotAPI:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'track_detection', 'show_tracks', 'show_signal', 'show_crop',
                                 'show_track_numbers',
                                 'track_colour', 'signal_colour', 'image']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + '/images/plot_on_chromatograms/*')

    def test_post_and_get_chromatogram_plot(self, track_detection_object, client):
        data = {
            'show_tracks': 'true',
            'show_signal': 'true',
            'show_crop': 'true',
            'show_track_numbers': 'true',
            'track_colour': '#000000',
            'signal_colour': '#0000ff',
        }
        track_detection_url = reverse('chromatogram', kwargs={'id': track_detection_object.id, })
        post_response = client.post(track_detection_url, data)
        post_response_content = json.loads(post_response.content).get('data')
        assert post_response.status_code == 200
        assert all(key in post_response_content for key in self.expected_response)

    def test_get_chromatogram_plot(self, plot_on_chromatogram_object, client):
        track_detection_url = reverse('chromatogram', kwargs={'id': plot_on_chromatogram_object.id, })
        response = client.get(track_detection_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)
