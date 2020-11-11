from django.core.signing import BadSignature
from rest_framework.permissions import IsAuthenticated
from ..base_view import BaseView
from ...library.constants import *
from ...library.helpers import decode_singing_dict
from crm.serializers import ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from ...models import User


class ChangePasswordView(BaseView):
    """
    View for user password change
    """
    permission_classes = (IsAuthenticated,)
    change_password_serializer = ChangePasswordSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        in kwargs must by signed dict with user id
        this id must be the same as user id in request
        request params:
            - password
        :return: json response
            http response codes:
                200 - ok, password changed
                400 - password validation error, view errors key for details
                403 - signature failed or invalid user id
            keys:
                success - true if password was changed and false otherwise
                errors - errors details if success is false
        """
        serializer = self.change_password_serializer(data=request.data)

        if not serializer.is_valid():
            return self.json_failed_response(errors=serializer.errors)

        data_from_request = serializer.data
        # todo look up in docs how to do it
        if not self.__is_user_password_change_allowed(request, **kwargs):
            return self.json_forbidden_response(
                errors={
                    SIGNATURE: 'bad signature or invalid user id'
                }
            )

        return self.__change_user_password(request.user, data_from_request[PASSWORD])

    def __change_user_password(self, user: User, new_password: str) -> Response:
        """
        changes user from request password
        """
        user.set_password(new_password)
        user.save()

        return self.json_success_response()

    def __is_user_password_change_allowed(self, request: Request, **kwargs) -> bool:
        """
        Check user id in url and user id in request.
        They must be the same for password change
        :return: True if id is the same
                 False if not or BadSignature appeared
        """
        try:
            user_id = decode_singing_dict(kwargs[DATA])[ID]
            return request.user.id == user_id
        except BadSignature:
            return False
