from django.contrib.auth.models import Group
from rest_framework import permissions

from .group_serializer import GroupSerializer
from ...library.constants import CHANGE_GROUP_EMAIL
from ...views import BaseView
from rest_framework.request import Request
from rest_framework.response import Response
from ...models import User
from ...serializers import UserSerializer
from ...library.helpers import send_dmc_email


class ChangeGroupView(BaseView):
    permission_classes = [permissions.IsAuthenticated]
    user_serializer = UserSerializer
    group_serializer = GroupSerializer
    template_name = CHANGE_GROUP_EMAIL

    def put(self, request: Request, user_id: int) -> Response:
        user_to_change, json_error = self.get_entity_or_json_error(User, user_id)

        if json_error:
            return json_error

        requested_user = User.objects.filter(pk=request.user.id).first()

        serializer = self.group_serializer(data=request.data,
                                           context={'user': user_to_change, 'request_user': requested_user})
        if serializer.is_valid():
            return self.__change_group_send_response(user_to_change, serializer)

        return self.json_failed_response(
            message=dict(
                message="Updating group failed"
            ),
            errors=serializer.errors
        )

    def __change_group_send_response(self, user: User, serializer: GroupSerializer) -> Response:
        old_group_name = user.groups.all().first().name
        new_group_name = serializer.data.get('group')
        group = Group.objects.filter(name=new_group_name).first()
        user.groups.clear()
        user.groups.add(group)

        send_dmc_email(self.template_name,
                       [user.email],
                       subject="Your group has been changed",
                       old_group_name=old_group_name,
                       new_group_name=new_group_name
                       )

        return self.json_success_response(
            message=dict(
                message="User's group changed successfully",
                user=self.user_serializer(user).data
            )
        )
