from django.contrib.auth import authenticate
from crm.views.base_view import BaseView
from ...library.constants import *
from ...library.helpers import generate_token_dict
from crm.serializers import UserSerializer
from crm.serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework.request import Request


class LoginView(BaseView):
    """
    View for login_service user
    """
    login_serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        request params:
            - email
            - password
        :return json response
            http response codes:
                200 - ok, login_service success
                400 - login_service failed - view errors in errors key
            keys:
                success - true if login_service was success and false otherwise
                errors - json of login_service errors if success if false
                token - json with access and refresh keys if success is true
                user - json with user data from serializer if success is true
        """
        serializer = self.login_serializer_class(data=request.data)

        if serializer.is_valid():
            return self.__login_user(serializer.data)
        else:
            return self.json_failed_response(errors=serializer.errors)

    def __login_user(self, data):
        """
        login_service user from request's email and password
        """
        try:
            user = authenticate(username=data[EMAIL], password=data[PASSWORD])

            return self.json_success_response(user=UserSerializer(user).data, token=generate_token_dict(user))
        except ValueError as e:
            errors = dict()

            for field, error in e.args[0].items():
                errors[field] = error

            return self.json_failed_response(errors=errors)
