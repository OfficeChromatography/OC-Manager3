from django.urls import reverse
import pytest
import json
from .utils import remove_files_from_local
from app.settings import MEDIA_ROOT

pytestmark = pytest.mark.django_db


class TestTrackInspectionAPI:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'track_detection', 'track_number', 'track_image', 'rgb_densitogram']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + '/images/inspection/rgb_densitogram/*')
        remove_files_from_local(MEDIA_ROOT + '/images/inspection/track/*')

    def test_post_track_inspection(self, track_detection_object, client):
        track_inspection_url = reverse('trackinspect', kwargs={'id': track_detection_object.id, 'track': 10})
        response = client.post(track_inspection_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_get_track_inspection(self, track_inspection_object, client):
        track_inspection_url = reverse('trackinspect', kwargs={'id': track_inspection_object.id, })
        response = client.get(track_inspection_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)
