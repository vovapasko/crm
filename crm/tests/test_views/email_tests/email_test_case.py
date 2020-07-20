from rest_framework import status

from main_app.models import User
from ..base_test_case import BaseTestCase


class EmailTestCase(BaseTestCase):
    url = '/email-registered/'
    non_existing_mail = "doesnotexist@mail.com"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = super().get_test_user()
        cls.manager_user = super().get_superuser()
        cls.users = User.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_unauthorised(self):
        client = self.get_api_client()
        response = client.get(
            self.generate_url(self.url, self.manager_user.email)
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_existing_email(self):
        client = self.get_api_client(user=self.user)
        response = client.get(
            self.generate_url(self.url, self.manager_user.email)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_key_in_dict(
            key="message",
            dict_to_check=self.get_json_content_from_response(response)
        )

    def test_non_existing_email(self):
        client = self.get_api_client(user=self.user)
        response = client.get(
            self.generate_url(self.url, self.non_existing_mail)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.check_key_in_dict(
            key="errors",
            dict_to_check=self.get_json_content_from_response(response)
        )
