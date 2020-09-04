from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, Group
import django.apps
from ...groups.groups import groups as main_app_groups
from ...groups.permissions import permissions as main_app_permissions
from ...library.constants import *
from ...library.exceptions import PermissionInUse


class Command(BaseCommand):
    """
    This command upgrade Group and Permission models according to changes in
    groups.py and permissions.py files in groups model.
    """
    help = 'implements groups in crm in models'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.models_names = []

    def handle(self, *args, **kwargs) -> None:
        self.models_names = [model.__name__.lower() for model in django.apps.apps.get_models()]

        self.__check_removed_permissions()  # in first place because permissions can be in groups and need check first
        self.__check_new_permissions()
        self.__check_new_groups()
        self.__check_removed_groups()

        self.stdout.write('\nEverything is up to date')

    def __check_new_groups(self) -> None:
        """
        Check whether new groups appeared and also check old groups changes
        """
        for group in main_app_groups:
            try:
                group_old = Group.objects.get(name=group)
                self.__upgrade_group(group_old, group)
            except ObjectDoesNotExist:  # need to create new group
                self.__create_new_group(group)

                self.stdout.write(f'Added new group {group} with {main_app_groups[group]} permissions')

    def __create_new_group(self, group_name) -> None:
        """
        creating new group and adding permissions from main_app_groups
        """
        group = Group(name=group_name)
        group.save()

        self.__add_permission_to_group(group)

    def __add_permission_to_group(self, group: Group) -> None:
        """
        adding permissions from main_app_groups
        :param group: Group object
        """
        for permission_codename in main_app_groups[group.name]:
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)

    def __check_removed_permissions(self) -> None:
        """
        check whether some permission was deleted
        before delete check whether permission is used in groups
        :raise PermissionInUse exception
        """
        for permission in Permission.objects.all():
            if not self.__is_permission_allowed_to_delete(permission):
                continue

            if self.__is_permission_in_groups(permission.codename):
                raise PermissionInUse(f'Permission {permission.codename} is used in groups. Delete it first.')

            permission.delete()

            self.stdout.write(f'Removed {permission.codename} permission')

    def __is_permission_allowed_to_delete(self, permission: Permission) -> None:
        """
        check if permission is deleted, if it's application's permission and if this permission is not model's
        """
        return permission.codename not in main_app_permissions \
               and permission.content_type.app_label == APP_NAME \
               and not self.__is_model_permission(permission.codename)

    def __check_new_permissions(self) -> None:
        """
        check whether new permissions was added and also check updates on all permissions
        """
        for permission in main_app_permissions:
            try:
                permission_old = Permission.objects.get(codename=main_app_permissions[permission][CODENAME])
                self.__upgrade_permission(permission, permission_old)
            except ObjectDoesNotExist:  # need to create new
                self.__create_new_permission(
                    codename=main_app_permissions[permission][CODENAME],
                    name=main_app_permissions[permission][NAME],
                    content_type=main_app_permissions[permission][CONTENT_TYPE]
                )

                self.stdout.write(f'Added new permission {main_app_permissions[permission][CODENAME]}')

    def __create_new_permission(self, codename, **kwargs) -> None:
        """
        create and save new permission
        """
        permission = Permission(codename=codename, **kwargs)
        permission.save()

    def __check_removed_groups(self) -> None:
        """
        check whether some group was deleted
        """
        for group in Group.objects.all():
            if group.name not in main_app_groups:
                self.__delete_group(group)

                self.stdout.write(f'Removed {group} group')

    def __delete_group(self, group) -> None:
        """
        delete group
        :param group: group name or Group obj
        """
        if isinstance(group, str):
            group = Group.objects.get(name=group)

        group.delete()

    def __upgrade_group(self, group_old: Group, group_new: str) -> None:
        """
        upgrade group info up to date
        """
        def upgrade_permissions(permissions_list_1: list, permissions_list_2: list, action) -> list:
            permissions_to_change = [
                permission_change
                for permission_change in permissions_list_1
                if permission_change not in permissions_list_2
            ]
            return self.__upgrade_group_permissions(group_old, permissions_to_change, action)

        messages = [f'Group {group_new} permission changes']

        permissions_from_db = [p.codename for p in group_old.permissions.all()]
        permissions_from_file = main_app_groups[group_new]

        # in db but not in file -> remove
        messages += upgrade_permissions(permissions_from_db, permissions_from_file, REMOVE)
        # in file but not in db -> add
        messages += upgrade_permissions(permissions_from_file, permissions_from_db, ADD)

        if len(messages) > 1:
            self.__print_messages(messages)

    def __upgrade_group_permissions(self, group: Group, permissions_list: list, action: str) -> list:
        """
        upgrade group permissions up to date
        :param group: group obj
        :param permissions_list: list of interested group permissions
        :param action: what need to do with this permissions (add, remove)
        :return:
        """
        messages = []

        for codename in permissions_list:
            getattr(group.permissions, action)(Permission.objects.get(codename=codename))

        if not len(permissions_list) == 0:
            messages.append(f'\t{action}ed {permissions_list}')

        return messages

    def __upgrade_permission(self, permission_new: Permission, permission_old: Permission) -> None:
        """
        upgrade permission info up to date
        """
        def check_attribute_changes(attribute_name: str) -> None:
            """
            check on changes given attribute in old and new permission
            :param attribute_name: name of attribute to check
            :return: list of massages
            """
            if not getattr(permission_old, attribute_name) == main_app_permissions[permission_new][attribute_name]:
                setattr(
                    permission_old,
                    attribute_name,
                    main_app_permissions[permission_new][attribute_name]
                )
                permission_old.save()

                messages.append(f'\tchanged {attribute_name} on <{getattr(permission_old, attribute_name)}>')

        messages = [f'Permission {permission_old.codename} changes']

        check_attribute_changes('name')
        check_attribute_changes('content_type')

        if not len(messages) == 1:
            self.__print_messages(messages)

    def __is_permission_in_groups(self, name: str) -> bool:
        """
        check whether any group contains permission with given codename
        :param name: codename of the permission
        :return: True if such a group exists
                 False otherwise
        """
        permission = Permission.objects.get(codename=name)

        for group_name in main_app_groups:
            group = Group.objects.get(name=group_name)
            if permission in group.permissions.all():
                return True

        return False

    def __is_model_permission(self, name: str) -> bool:
        """
        Every model has some default permissions. This method check whether permission refers to some model in app
        :param name: codename of permission
        :return: True if permission refers to app model
                 False if no
        """
        permission_name, model_name = name.split('_')

        return permission_name in PERMISSIONS_PREFIXES and model_name in self.models_names

    def __print_messages(self, messages: list) -> None:
        """
        print messages interminal
        :param messages: list of str
        """
        for message in messages:
            self.stdout.write(message)
