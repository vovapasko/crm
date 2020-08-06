from rest_framework import status

from crm.tests.base_test_case import BaseTestCase
from .test_data import *


class LoginTestCase(BaseTestCase):
    url = '/login/'
    keys_to_check = ['user', 'token']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = super().get_test_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_login(self):
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data=correct_login_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_keys_in_dict(
            data=self.get_json_content_from_response(response),
            keys_to_check=self.keys_to_check
        )

    def test_login_no_password(self) -> None:
        self.__test_login_no_elements(["password"], no_password_login_data)

    def test_login_no_email(self) -> None:
        self.__test_login_no_elements(["email"], no_email_login_data)

    def test_login_no_email_password(self) -> None:
        self.__test_login_no_elements(["email", "password"], empty_data)

    def __test_login_no_elements(self, element_key_list: list, request_data: dict) -> None:
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data=request_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for element_key in element_key_list:
            self.assertIn(
                member=element_key,
                container=self.get_errors_dict_from_response(response)
            )

    def test_non_existing_user_login(self) -> None:
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data=non_existing_user
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member="email",
            container=self.get_errors_dict_from_response(response)
        )

    def test_incorrect_password_login(self) -> None:
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data=incorrect_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member="password",
            container=self.get_errors_dict_from_response(response)
        )
