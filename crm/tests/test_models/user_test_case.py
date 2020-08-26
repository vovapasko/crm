from django.test import TestCase
from ...models import User
from django.contrib.auth.models import Group
from crm.library.fixtures.fixtures import *
from ...library.constants import SUPERUSER, ADMIN, MANAGER
from django.core.management import call_command


class UserTestCase(TestCase):
    def setUp(self):
        self.__create_groups()
        self.__create_users()

    def test_superuser_group(self):
        expected_group, actual_group = self.__get_expected_actual_group_by_id(TEST_SUPERUSER_EMAIL, SUPERUSER)
        self.assertEqual(actual_group, expected_group)

    def test_admin_user_group(self):
        expected_group, actual_group = self.__get_expected_actual_group_by_id(TEST_ADMIN_EMAIL, ADMIN)
        self.assertEqual(actual_group, expected_group)

    def test_manager_user_group(self):
        expected_group, actual_group = self.__get_expected_actual_group_by_id(TEST_MANAGER_EMAIL, MANAGER)
        self.assertEqual(actual_group, expected_group)

    def __get_expected_actual_group_by_id(self, user_email, group_name):
        user = User.objects.get(email=user_email)
        expected_group = self.__get_expected_group(group_name)
        actual_group = user.groups.all().first()
        return expected_group, actual_group

    def __get_expected_group(self, group_name):
        return Group.objects.filter(name=group_name).first()

    def __create_users(self):
        User.objects.create_superuser(
            email=TEST_SUPERUSER_EMAIL,
            password=TEST_SUPERUSER_PASSWORD
        )

        User.objects.create_admin_user(
            email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        User.objects.create_manager_user(
            email=TEST_MANAGER_EMAIL,
            password=TEST_MANAGER_PASSWORD
        )

    def __create_groups(self):
        call_command('upgrade_groups')
