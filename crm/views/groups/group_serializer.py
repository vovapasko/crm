from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ...library.constants import SUPERUSER, ADMIN


class GroupSerializer(serializers.Serializer):
    group = serializers.CharField()

    def validate_group(self, value: str):
        """
        value - name of the group
        """
        user = self.context.get('user')
        request_user = self.context.get('request_user')
        current_user_group = request_user.groups.first()

        self.__check_user(user, request_user.id)
        requested_group = Group.objects.filter(name=value).first()
        self.__check_valid_group(requested_group, value)
        self.__check_group_access(current_user_group)
        self.__check_user_group_rank(requested_group, current_user_group)

        return value

    def __check_valid_group(self, group, group_name):
        if group is None:
            raise ValidationError(f"Group {group_name} does not exist")

    def __check_group_access(self, group):
        if group.name != SUPERUSER and group.name != ADMIN:
            raise ValidationError("Only Superuser or Admin can change the group")

    def __check_user_group_rank(self, requested_group, current_group):
        # user can not change group to the group with higher rank than his
        current_group_index = current_group.id
        requested_index = requested_group.id

        if current_group_index > requested_index:
            raise ValidationError("You don't have permission to change the group higher then your's current")

    def __check_user(self, user, id_to_change):
        if user.id == id_to_change:
            raise ValidationError("You can't change the group for yourself")
