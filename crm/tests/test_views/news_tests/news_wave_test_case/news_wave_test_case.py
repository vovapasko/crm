from rest_framework import status
from rest_framework.reverse import reverse

from crm.tests.base_test_case import BaseTestCase
from crm.models import NewsWave, NewsProject


class NewsWaveTestCase(BaseTestCase):
    url = reverse('crm:newswaves')
    project_get_parameter = 'project'
    wave_get_parameter = 'wave'

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
            {
                self.project_get_parameter: project.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
