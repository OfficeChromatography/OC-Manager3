from django.urls import reverse
from .utils import remove_files_from_local
from app.settings import MEDIA_ROOT
import pytest
import json

pytestmark = pytest.mark.django_db


class TestHeatmapAPI:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'track_detection', 'reference', 'heatmap']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + f'/images/heatmap/*')

    def test_post_heatmap(self, track_detection_object, client):
        heatmap_url = reverse('heatmap', kwargs={'id': track_detection_object.id})
        response = client.post(heatmap_url, {'reference': '1-5,7'})
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_get_pca(self, heatmap_object, client):
        heatmap_url = reverse('heatmap', kwargs={'id': heatmap_object.id})
        response = client.get(heatmap_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)
