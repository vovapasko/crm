from crm.models import Contractor, Hashtag, NewsEmail, Client
from crm.tests.base_test_case import BaseTestCase
from rest_framework.reverse import reverse
from rest_framework import status


class NewsProjectViewTestCase(BaseTestCase):
    url = reverse('crm:newsprojects')

    CORRECT_INIT_PROJECT_DATA = {
        "name": "My project",
        "budget": 1234,
        "manager_id": 1
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_user = cls.get_admin_user()
        cls.test_manager = cls.get_admin_user()
        cls.test_contractor = Contractor.objects.first()
        cls.test_hashtag = Hashtag.objects.first()
        cls.test_email = NewsEmail.objects.first()
        cls.test_client = Client.objects.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_news_project_authenticated(self):
        client = self.get_api_client(user=self.test_user)
        response = client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_news_project_authenticated(self):
    #     client = self.get_api_client(user=self.test_user)
    #     correct_project_data = self.CORRECT_INIT_PROJECT_DATA
    #     correct_project_data.update(
    #         {
    #             "client": self.test_client,
    #             "hashtags": self.test_hashtag,
    #             "contractors": self.test_contractor,
    #             "emails": self.test_email
    #         }
    #     )
    #     response = client.post(
    #         path=self.url,
    #         data=correct_project_data
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_news_project_unauthenticated(self):
        client = self.get_api_client()
        self._test_request_method_clients(
            method=client.get,
            url=self.url,
            response_code=status.HTTP_401_UNAUTHORIZED
        )