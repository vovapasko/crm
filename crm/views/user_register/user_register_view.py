from rest_framework import status
from ...library.helpers import decode_singing_dict, generate_token_dict
from ..base_view import BaseView
from .user_register_serializer import UserRegisterSerializer
from ...serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from ...library.helpers import get_id_or_exception
from ...library.constants import MESSAGE_JSON_KEY
from rest_framework.response import Response
from rest_framework.request import Request


class UserRegisterView(BaseView):
    user_register_serializer = UserRegisterSerializer
    user_serializer = UserSerializer

    # todo if pass to request signed id of other user, method will overwrite data in existing user. Fix it
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        request params:
            - first_name
            - last_name
            - password
            - password confirm
        :return json response
            http response codes:
                200 - ok, data is valid and is updated
                400 - registration failed, validation failed
                404 - if link was in incorrect format

            keys:
                status - response status
                token - JWT token
                user - user data from user_serializer
                errors - contains errors during this request
        """
        try:
            user_id = get_id_or_exception(**kwargs)
        except ObjectDoesNotExist:
            return self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors={
                    "LINK_ERROR": "Link is incorrect"
                }
            )

        serializer = self.user_register_serializer(data=request.data)

        if serializer.is_valid():
            return self.__register_user_send_response(user_id, serializer)
        else:
            return self.json_failed_response(
                errors=serializer.errors
            )

    def __register_user_send_response(self, user_id: int, serializer: UserRegisterSerializer) -> Response:
        user = self.get_user_object(user_id)
        serializer.update(user, serializer.data)

        return self.json_success_response(
            message={
                MESSAGE_JSON_KEY: "User registered successfully",
            },
            token=generate_token_dict(user),
            user=self.user_serializer(user).data
        )
