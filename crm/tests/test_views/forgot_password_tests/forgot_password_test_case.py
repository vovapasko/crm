from rest_framework import status
from rest_framework.reverse import reverse

from crm.tests.base_test_case import BaseTestCase


class ForgotPasswordTestCase(BaseTestCase):
    url = reverse('crm:forgot-password')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = cls.get_admin_user()
        cls.existing_email = cls.user.email
        cls.non_existing_email = 'not_existing@mail.com'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_forgot_password_post_wrong_email(self):
        self.__send(email=self.non_existing_email, status_code=status.HTTP_404_NOT_FOUND)

    def test_forgot_password_post_correct_email(self):
        self.__send(email=self.existing_email, status_code=status.HTTP_200_OK)

    def __send(self, email: str, status_code: int) -> None:
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data={'email': email}
        )
        self.assertEqual(response.status_code, status_code)
