from django.urls import reverse
import pytest
import json
from .utils import remove_files_from_local
from app.settings import MEDIA_ROOT

pytestmark = pytest.mark.django_db

class TestPCAAPI:

    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'track_detection', 'reference', 'explained_variance', 'pca']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + f'/images/pca_analysis/explained_variance/*')
        remove_files_from_local(MEDIA_ROOT + f'/images/pca_analysis/pca/*')


    def test_post_pca(self, track_detection_object, client):
        pca_url = reverse('pca', kwargs={'id': track_detection_object.id})
        response = client.post(pca_url, {'reference': '1-5,7'})
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_get_pca(self, pca_object, client):
        pca_url = reverse('pca', kwargs={'id': pca_object.id})
        response = client.get(pca_url)
        response_content = json.loads(response.content).get('data')
        print(response_content)
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)
