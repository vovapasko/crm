from django.contrib.auth.models import Group

from crm.library.helpers import groups_cascade_down
from crm.tests.base_test_case import BaseTestCase


class GroupsCascadeDownTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.superuser_group = cls.get_superuser().groups.first()
        cls.admin_group = cls.get_admin_user().groups.first()
        cls.manager_group = cls.get_manager_user().groups.first()
        cls.guest_group = cls.get_guest_user().groups.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_groups_cascade_down_for_groups(self):
        self.__test_for_group(
            group=self.superuser_group,
            expected_len=4,
            expected_list=[
                self.superuser_group.name,
                self.admin_group.name,
                self.manager_group.name,
                self.guest_group.name
            ]
        )
        self.__test_for_group(
            group=self.admin_group,
            expected_len=3,
            expected_list=[
                self.admin_group.name,
                self.manager_group.name,
                self.guest_group.name
            ]
        )
        self.__test_for_group(
            group=self.manager_group,
            expected_len=2,
            expected_list=[
                self.manager_group.name,
                self.guest_group.name
            ]
        )
        self.__test_for_group(
            group=self.guest_group,
            expected_len=1,
            expected_list=[
                self.guest_group.name
            ]
        )

    def __test_for_group(self, *, group: Group, expected_len: int, expected_list: list) -> None:
        actual = groups_cascade_down(group)
        self.assertEqual(len(actual), expected_len)
        self.assertEqual(actual, expected_list)
