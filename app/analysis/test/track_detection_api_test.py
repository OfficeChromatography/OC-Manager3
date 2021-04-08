import pytest
import json

from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestTrackDetectionAPI:
    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'number_of_tracks', 'track_width', 'bands_start', 'front']

    def test_post_track_detection(self, image_object, client):
        data = {
            'image': image_object.id,
            'number_of_tracks': 20,
            'track_width': 19,
            'bands_start': 12,
            'front': 164,
        }

        url = reverse('trackdetection', kwargs={'id': data.get('image'), })
        response = client.post(url, data)
        response_content = json.loads(response.content).get('data')

        assert all(key in response_content for key in self.expected_response)
        assert response.status_code == 200

    def test_get_track_detection(self, track_detection_object, client):
        url = reverse('trackdetection', kwargs={'id': track_detection_object.id, })
        response = client.get(url)
        response_content = json.loads(response.content).get('data')
        assert all(key in response_content for key in self.expected_response)
        assert response.status_code == 200
