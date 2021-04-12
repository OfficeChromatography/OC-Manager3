from django.urls import reverse
import pytest
import json
from .utils import remove_files_from_local
from app.settings import MEDIA_ROOT

pytestmark = pytest.mark.django_db


class TestHcaAPI:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'reference', 'hca_tracks', 'num_clusters', 'hca']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + f'/images/hca_analysis/tracks/*')
        remove_files_from_local(MEDIA_ROOT + f'/images/hca_analysis/hca/*')

    def test_post_hca(self, track_detection_object, client):
        hca_url = reverse('hca', kwargs={'id': track_detection_object.id})
        response = client.post(hca_url, {'reference': '1-5,7', 'num_clusters': 5})
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_get_hca(self, hca_object, client):
        hca_url = reverse('hca', kwargs={'id': hca_object.id})
        response = client.get(hca_url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)


 #    def test_get_pca(self, heatmap_object, client):
 #        heatmap_url = reverse('heatmap', kwargs={'id': heatmap_object.id})
 #        response = client.get(heatmap_url)
 #        response_content = json.loads(response.content).get('data')
 #        assert response.status_code == 200
 #        assert all(key in response_content for key in self.expected_response)
 #
 # def _post_hca(self):
 #        post_response = self._track_detect()
 #        post_response_content = json.loads(post_response.content).get('data')
 #        hca_url = reverse('hca', kwargs={'id': post_response_content.get('id')})
 #        return self.client.post(hca_url, {'reference': '1-5,7', 'num_clusters': 5})
 #
 #
 # def test_post_hca(self):
 #        post_response = self._post_hca()
 #        post_response_content = json.loads(post_response.content).get('data')
 #        assert post_response.status_code == 200
 #        assert all(key in post_response_content for key in ['id',
 #                                                            'hca_tracks',
 #                                                            'num_clusters',
 #                                                            'hca', ])
