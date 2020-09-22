from crm.models import User
from rest_framework import status

from crm.tests.base_test_case import BaseTestCase


class UsersTestCase(BaseTestCase):
    """
    According to business logic all users may see the full list of users.
    Only superuser can delete users.
    """
    url = '/users/'

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.superuser = super().get_superuser()
        cls.admin_user = super().get_admin_user()
        cls.manager_user = super().get_manager_user()
        cls.client_user = super().get_guest_user()
        cls.users = User.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_admin_users_view(self) -> None:
        self.__test_users_list_authorised(self.admin_user)

    def test_superusers_view(self) -> None:
        self.__test_users_list_authorised(self.superuser)

    def test_manager_users_view(self) -> None:
        self.__test_users_list_authorised(self.manager_user)

    def test_client_users_view(self) -> None:
        self.__test_users_list_authorised(self.client_user)

    def __test_users_list_authorised(self, login_user: User) -> None:
        client = self.get_api_client(user=login_user)
        response = client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.get_json_content_from_response(response).get('count'),
            self.users.count()
        )

    def test_unauthorised(self) -> None:
        client = self.get_api_client()
        response = client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_superuser_by_superuser(self) -> None:
        # trying superuser to delete himself. Server should prevent it
        client = self.get_api_client(user=self.superuser)
        response = client.delete(
            path=self.generate_url(self.url, self.superuser.id)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            member="errors",
            container=self.get_json_content_from_response(response)
        )

    def test_delete_admin_by_superuser(self) -> None:
        self.__test_delete_user_by_superuser(self.admin_user)

    def test_delete_manager_by_superuser(self) -> None:
        self.__test_delete_user_by_superuser(self.manager_user)

    def test_delete_client_by_superuser(self) -> None:
        self.__test_delete_user_by_superuser(self.client_user)

    def __test_delete_user_by_superuser(self, user_to_delete: User) -> None:
        client = self.get_api_client(user=self.superuser)
        response = client.delete(
            path=self.generate_url(self.url, user_to_delete.id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            member='message',
            container=self.get_json_content_from_response(response)
        )
