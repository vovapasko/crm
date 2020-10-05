from rest_framework import status
from rest_framework.reverse import reverse

from crm.tests.base_test_case import BaseTestCase
from email_app.apps import EmailAppConfig


class GmailCredentialsClearViewTestCase(BaseTestCase):
    url = reverse(f'{EmailAppConfig.name}:gmail-creds-clear')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admin_user = cls.get_admin_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_post_revoke_token_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        # response = client.post(
        #     path=self.url
        # )
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth_unauthorised(self):
        client = self.get_api_client()
        response = client.post(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
