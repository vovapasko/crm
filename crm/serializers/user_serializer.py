from drf_writable_nested import UniqueFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from crm.library.helpers import groups_cascade_down as get_groups_cascade_down
from crm.models import User


class UserSerializer(WritableNestedModelSerializer):
    groups_cascade_down = SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'user_permissions']
        depth = 1

    def get_groups_cascade_down(self, obj):
        """
        list of groups names cascade down from user's group
        :param obj: user for attribute generation
        :return: list of groups names
        """
        return get_groups_cascade_down(obj.groups.first())
