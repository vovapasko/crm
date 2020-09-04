from typing import Type

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db.models.query import QuerySet

from crm.library.constants import ADMIN
from crm.models import Client, Hashtag, NewsEmail, NewsProject, NewsWave


class Command(BaseCommand):
    help = 'Provide groups with permissions except custom ones which were ' \
           'created in create_groups command'

    def handle(self, *args, **kwargs):
        self.__edit_admin_group()

    def __edit_admin_group(self):
        admin_group = Group.objects.get(name=ADMIN)
        self.__provide_permissons_for_models(
            group=admin_group,
            models_list=[
                Client,
                Hashtag,
                NewsEmail,
                NewsProject,
                NewsWave
            ]
        )

    def __provide_permissons_for_models(self, *, group: Group, models_list: list):
        for model in models_list:
            model_content_type = self.__get_content_type_by_model(model=model)
            model_permissions = Permission.objects.filter(content_type=model_content_type)
            self.__remove_delete_exception(model_permissions)
            self.__add_permissions_to_group(group, model_permissions)

    @staticmethod
    def __add_permissions_to_group(group: Group, permissions: list):
        group.permissions.add(permissions)

    @staticmethod
    def __get_content_type_by_model(*, app_label: str = 'crm', model: Type[Model]):
        return ContentType.objects.get(app_label=app_label, model=model.__name__.lower())

    @staticmethod
    def __remove_delete_exception(permissions_list: QuerySet):
        for permission in permissions_list:
            if 'delete' in permission.codename:
                permissions_list.exclude(id=permission.id)
