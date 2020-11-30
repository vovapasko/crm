from rest_framework import status
from rest_framework.reverse import reverse

from crm.tests.base_test_case import BaseTestCase
from crm.models import NewsWave, NewsProject
from crm.views.news.news_burst.news_wave_view import NewsWaveView


class NewsWaveTestCase(BaseTestCase):
    url = reverse('crm:newswaves')
    project_get_parameter = NewsWaveView.project_id_get_request_param
    wave_get_parameter = NewsWaveView.wave_id_get_request_param

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.all_waves = NewsWave.objects.all()
        cls.admin_user = cls.get_admin_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_news_wave_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        project = NewsProject.objects.first()
        response = client.get(
            self.url,
            data={
                self.project_get_parameter: project.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_news_wave_unauthorised(self):
        client = self.get_api_client()
        response = client.post(
            self.url,
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_news_wave_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        response = client.post(
            self.url,
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
