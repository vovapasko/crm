from django.core import signing
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from ..base_view import BaseView
from ...library.constants import *
from ...library.helpers import send_dmc_email, is_user_allowed_cascade_down
from ...library.helpers.views import format_link
from ...models import User
from crm.serializers import InviteNewUserSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from typing import Dict

from crm.serializers import UserSerializer


class InviteNewUserView(BaseView):
    """
    view for inviting new users
    permission_required: CAN_INVITE_NEW_USER_PERMISSION
    """
    permission_classes = (IsAuthenticated,)
    template_email_name = REGISTER_NEW_USER_EMAIL
    permission_required = [CAN_INVITE_NEW_USER_PERMISSION]
    invite_new_user_serializer_class = InviteNewUserSerializer
    user_serializer = UserSerializer
    objects = User.objects
    rules = {
        SUPERUSER: objects.create_superuser,
        ADMIN: objects.create_admin_user,
        MANAGER: objects.create_manager_user,
        GUEST: objects.create_guest_user
    }

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        request params:
            - email
            - group (group name)
        :return json response
            http response codes:
                200 - ok, invitation email sent
                400 - failed, validation error, view errors key
                403 - failed, permission denied
            keys:
                success - true if invitation email sent and false otherwise
                errors - json of errors if success is false
        """
        serializer = self.invite_new_user_serializer_class(data=request.data)

        if not serializer.is_valid():
            return self.json_failed_response(errors=serializer.errors)

        data_from_request = serializer.data

        if not is_user_allowed_cascade_down(request.user, data_from_request[GROUP]):
            return self.json_forbidden_response(
                errors={
                    PERMISSION: 'permission denied'
                }
            )

        return self.__register_and_send_email(request, data_from_request)

    def __register_and_send_email(self, request: Request, data: Dict) -> Response:
        """
        register new user and send him an email with link to complete registrations
        """
        try:
            user = self.__add_new_user(data[EMAIL], data[GROUP])
            user_id = user.id
        except IntegrityError:
            return self.json_failed_response(
                errors={
                    EMAIL: 'Such an email is already registered'
                }
            )
        new_user = User.objects.filter(pk=user_id).first()
        self.__send_email(request, data[EMAIL], user_id)

        return self.json_success_response(
            message={
                MESSAGE_JSON_KEY: "Users are handled successfully"
            },
            user=self.user_serializer(new_user).data
        )

    def __send_email(self, request: Request, email: str, user_id: int):
        """
        send email with link to complete registration
        :param email: user email
        :param user_id: id for signing
        """
        data = signing.dumps(dict(id=user_id))

        url = format_link(INVITE_NEW_USER_LINK)
        send_dmc_email(
            self.template_email_name,
            [email],
            subject='TSG invitation',
            link=f'{url}/{data}'
            # link format <Host>/<path to password change page>/<data with user email adn role id>
        )

    def __add_new_user(self, email: str, group_name: str) -> int:
        """
        user_register new user by email and set group by is
        :param email: user email from request
        :param group_id: user group id from request
        :return: registered user
        """

        # What is written below is the substitution of long if chain
        # rule is the function which should be called according to group name
        rule = self.rules.get(group_name)
        if rule:
            return rule(email, '')

        raise ValidationError("Invalid group or email")
