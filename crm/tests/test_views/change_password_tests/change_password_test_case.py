from rest_framework import status

from crm.library.constants import SIGNATURE
from crm.tests.base_test_case import BaseTestCase
from crm.models import User
from .test_data import *


class ChangePasswordTestCase(BaseTestCase):
    url = '/change-pass/'
    # convenient way to access data in test_data and provide testing response message with message in data
    password_data_key = "password_data"
    key_to_check = "password"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_admin_user(**init_user_data)
        cls.other_user = super().get_guest_user()
        cls.correct_link = cls.generate_encoded_link(cls, cls.url, cls.user)
        cls.users = User.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_change_password_correct_link_unauthorised(self):
        client = self.get_api_client()
        response = client.post(
            path=self.correct_link,
            data=new_user_correct_password
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            member='detail',
            container=self.get_json_content_from_response(response)
        )

    def test_change_password_incorrect_link(self):
        # in this case the id of other user will be encoded in link. this should cause 400 code
        client = self.get_api_client(user=self.user)
        incorrect_link = self.generate_encoded_link(self.url, self.other_user)
        response = client.post(
            path=incorrect_link,
            data=new_user_correct_password
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            member=SIGNATURE,
            container=self.get_errors_dict_from_response(response)
        )

    def test_correct_password(self):
        client = self.get_api_client(user=self.user)
        response = client.post(
            path=self.correct_link,
            data=new_user_correct_password
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # todo hash of the same passwords has to be the same. Find out why it doesn't work here
        # new_password_from_user = self.user.password
        # hashed_new_password = make_password(new_user_correct_password.get('password'))
        # self.assertEqual(new_password_from_user, hashed_new_password)

    def test_short_password(self):
        self.__test_change_wrong_format_passwords_correct_link(
            password_data=short_password_data,
        )

    def test_no_number_password(self):
        self.__test_change_wrong_format_passwords_correct_link(
            password_data=no_number_data,
        )

    def test_no_letter_password(self):
        self.__test_change_wrong_format_passwords_correct_link(
            password_data=no_letters_data,
        )

    def test_no_letter_with_symbol_password(self):
        self.__test_change_wrong_format_passwords_correct_link(
            password_data=no_letters_with_symbol_data
        )

    def test_one_case_password(self):
        self.__test_change_wrong_format_passwords_correct_link(
            password_data=one_case_data,
        )

    def __test_change_wrong_format_passwords_correct_link(self,
                                                          password_data: dict,
                                                          password_data_key: str = password_data_key,
                                                          key_to_check_values: str = key_to_check) -> None:
        client = self.get_api_client(user=self.user)
        response = client.post(
            path=self.correct_link,
            data=password_data.get(password_data_key)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.check_values(
            initial_data=self.get_errors_dict_from_response(response),
            response_data=password_data,
            key=key_to_check_values
        )
