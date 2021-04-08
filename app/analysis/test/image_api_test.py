from app.settings import MEDIA_ROOT
from django.urls import reverse
from django.core.files import File
from .utils import remove_files_from_local, IMAGE_PATH
import json
import pytest
from .fixtures import image_object

pytestmark = pytest.mark.django_db

@pytest.mark.usefixtures("image_object")
class TestImageAPI:
    @classmethod
    def setup_class(cls):
        cls.expected_response = ['id', 'image', 'filename', 'uploader', 'note']

    @classmethod
    def teardown_class(cls):
        remove_files_from_local(MEDIA_ROOT + '/images/test_image_*')

    def test_get_image(self, image_object, client):
        url = reverse('image', kwargs={'id': image_object.id, })
        response = client.get(url)
        response_content = json.loads(response.content).get('data')
        assert response.status_code == 200
        assert all(key in response_content for key in self.expected_response)

    def test_post_image(self, client):
        with open(IMAGE_PATH, 'rb') as image:
            data = {
                'image': File(image),
                'filename': 'test',
            }
            url = reverse('image')
            response = client.post(url, data)
            response_content = json.loads(response.content).get('data')
            print(response_content)
            assert response.status_code == 200
            assert all(key in response_content for key in self.expected_response)
