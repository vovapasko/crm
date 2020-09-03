from ..constants.permissions import GROUPS_FOR_CASCADE
from django.contrib.auth.models import Group
from ...models import User
from ..constants import SUPERUSER, MANAGER, ADMIN, GUEST


def groups_cascade_down(group: Group) -> list:
    """
    for given group returns list of groups names which is cascade down from given group
    :param group: group name or Group from django models
    :return: list of groups name
    """

    def __cascade(group_type, value) -> list:
        if isinstance(group, group_type):
            return GROUPS_FOR_CASCADE[GROUPS_FOR_CASCADE.index(value) + 1:]

    return __cascade(str, group) or __cascade(Group, group.name) or list()


def is_user_allowed_cascade_down(user: User, group_name: str) -> bool:
    """
    check if user allowed to make any changes on other users with group name group_name
    if allowed only cascade down permission
    :param user: user from User model
    :param group_name: name of group to check
    :return: True if user can do changes cascade down on users with group_name
             False otherwise
    """
    return group_name in groups_cascade_down(user.groups.first())


def get_name_from_permission(permission: str) -> str:
    """
    codename from app_name.codename of permission
    :param permission: permission from view's permission_required
    :return: permission codename
    """
    app_name, permission_name = permission.split('.')
    return permission_name


def group_has_access(group_name):
    return group_name == SUPERUSER or group_name == ADMIN
