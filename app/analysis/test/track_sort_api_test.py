import pytest
import json

from django.urls import reverse
from .utils import remove_files_from_local
from app.settings import MEDIA_ROOT

pytestmark = pytest.mark.django_db


class TestTrackSort:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'track_detection', 'rf', 'sorted_image']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + '/images/track_sort/*')

    def test_post_track_sort(self, track_detection_object, client):
        track_sort_url = reverse('tracksort', kwargs={'id': track_detection_object.id})
        response = client.post(track_sort_url, {'rf': '0.7', })
        response_content = json.loads(response.content).get('data')

        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_get_track_sort(self, track_sort_object, client):
        track_sort_url = reverse('tracksort', kwargs={'id': track_sort_object.id})
        response = client.get(track_sort_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)
