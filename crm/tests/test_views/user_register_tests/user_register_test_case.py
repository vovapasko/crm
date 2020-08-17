from django.core import signing
from rest_framework import status

from ....models import User
from crm.tests.base_test_case import BaseTestCase
from .test_data import *


class UserRegisterTestCase(BaseTestCase):
    url = '/confirm-user/'
    keys_to_check_in_user = ['first_name', 'last_name']
    keys_to_check_in_correct_response = ['success', 'message', 'user', 'token']
    keys_to_check_in_incorrect_response = ['errors']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_user = User.objects.create_superuser(**new_user_base_data)
        cls.non_existing_id = -1
        cls.admin = cls.get_admin_user()
        cls.correct_invite_link = cls.generate_encoded_link(cls, cls.url, cls.new_user)
        cls.users = User.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_base_data_empty(self):
        """
        First name, last name should be empty
        """
        self.assertEqual(self.new_user.first_name, '')
        self.assertEqual(self.new_user.last_name, '')

    def test_register_user_correct_data(self):
        client = self.get_api_client()
        response = client.post(
            path=self.correct_invite_link,
            data=correct_register_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_keys_in_dict(
            data=self.get_json_content_from_response(response),
            keys_to_check=self.keys_to_check_in_correct_response
        )
        self.__check_first_last_name(response)

    def test_register_user_incorrect_data(self):
        client = self.get_api_client()
        # incorrect because
        incorrect_link = self.__generate_encoded_link_by_int(self.url, self.non_existing_id)
        response = client.post(
            path=incorrect_link,
            data=correct_register_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def __check_first_last_name(self, response):
        self.check_values_many_keys(
            initial_data=correct_register_data,
            response_data=self.get_json_content_from_response(response).get('user'),
            keys=self.keys_to_check_in_user
        )

    def __generate_encoded_link_by_int(self, url: str, id: int) -> str:
        data = signing.dumps(dict(id=id))
        return f'{url}{data}'
