from typing import Type

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Model
from crm.library.constants import ADMIN, MANAGER
from crm.models import Client, Hashtag, NewsEmail, NewsProject, NewsWave, Contractor


class Command(BaseCommand):
    help = 'Provide groups with permissions except custom ones which were ' \
           'created in create_groups command'

    def handle(self, *args, **kwargs):
        self.__edit_admin_group()
        self.__edit_manager_group()

    def __edit_admin_group(self):
        admin_group = self.__get_group(ADMIN)
        self.__provide_permissons_for_models(
            group=admin_group,
            without_delete_permission_models_list=[
                Client,
                Contractor
            ],
            all_permissions_model_list=[
                Hashtag,
                NewsEmail,
                NewsProject,
                NewsWave
            ]
        )

    def __edit_manager_group(self):
        manager_group = self.__get_group(MANAGER)
        self.__provide_permissons_for_models(
            group=manager_group,
            without_delete_permission_models_list=[
                Hashtag,
                NewsEmail,
                NewsProject,
                NewsWave,
                Client,
                Contractor
            ]
        )

    def __provide_permissons_for_models(
            self,
            *,
            group: Group,
            all_permissions_model_list: list = [],
            without_delete_permission_models_list: list,
    ):
        """By default all delete_ permissions are removed in models list.
        If you want to leave delete_ permission for this model and for this group, add the model
        to all_permissions_models_list"""
        for model in all_permissions_model_list:
            self.__moderate(model, group)

        for model in without_delete_permission_models_list:
            self.__moderate(model, group, remove_delete=True)

    def __moderate(self, model, group, remove_delete: bool = False):
        model_content_type = self.__get_content_type_by_model(model=model)
        model_permissions = list(Permission.objects.filter(content_type=model_content_type))
        if remove_delete:
            self.__remove_delete_permission(model_permissions)
        self.__add_permissions_to_group(group, model_permissions)

    @staticmethod
    def __add_permissions_to_group(group: Group, permissions: list):
        group.permissions.add(*permissions)

    @staticmethod
    def __get_content_type_by_model(*, app_label: str = 'crm', model: Type[Model]):
        return ContentType.objects.get(app_label=app_label, model=model.__name__.lower())

    @staticmethod
    def __remove_delete_permission(permissions_list: list) -> None:
        for permission in permissions_list:
            if 'delete' in permission.codename:
                permissions_list.remove(permission)

    @staticmethod
    def __get_group(group_name: str):
        return Group.objects.get(name=group_name)
