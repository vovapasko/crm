from rest_framework.reverse import reverse
from crm.models import NewsEmail
from rest_framework import status
from .test_data import *

from crm.tests.base_test_case import BaseTestCase


class NewsEmailTestCase(BaseTestCase):
    url = reverse('crm:news-emails')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.emails = NewsEmail.objects.all()
        cls.admin_user = cls.get_admin_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_email_unauthorised(self):
        client = self.get_api_client()
        response = client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_email_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        response = client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_email_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        response = client.post(
            path=self.url,
            data=CORRECT_NEWS_EMAIL
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_no_codeword_news_email(self):
        self.__test_post_incorrect_news_email(NO_CODEWORD_NEWS_EMAIL)

    def test_post_no_email_news_email(self):
        self.__test_post_incorrect_news_email(NO_EMAIL_NEWS_EMAIL)

    def __test_post_incorrect_news_email(self, post_data):
        client = self.get_api_client(user=self.admin_user)
        response = client.post(
            path=self.url,
            data=post_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
