from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from crm.library.helpers.views import unconvert_uid
from crm.models import User
from crm.views.base_view import BaseView
from crm.serializers.security import ConfirmPasswordSerializer


class ForgotPasswordConfirmView(BaseView):
    serializer_class = ConfirmPasswordSerializer

    password_param = 'password'
    uid_param = 'uid'
    token_param = 'token'

    password_swagger_param = openapi.Parameter(name=password_param, in_=openapi.IN_QUERY,
                                               description="Password of user which need to reset",
                                               required=True, type=openapi.TYPE_STRING)
    uid_swagger_param = openapi.Parameter(name=uid_param, in_=openapi.IN_QUERY,
                                          description="ID of user who password need to reset."
                                                      "It goes in url in format /{uid}/{token}",
                                          required=True, type=openapi.TYPE_STRING)
    token_swagger_param = openapi.Parameter(name=token_param, in_=openapi.IN_QUERY,
                                            description="token of user who password need to reset."
                                                        "It goes in url in format /{uid}/{token}",
                                            required=True, type=openapi.TYPE_STRING)

    response_404 = openapi.Response(
        description="404 Error in dict {errors: Error type}. No such a user with this email",
        examples={
            404: {
                "non_field_errors": [
                    "Incorrect token or uid"
                ]
            }
        }
    )
    response_200 = openapi.Response(
        description="Password was successfully changed",
        examples={
            200: {
                "Success": "Password is changed!"
            }
        },
    )

    @swagger_auto_schema(manual_parameters=[password_swagger_param, uid_swagger_param, token_swagger_param],
                         responses={200: response_200, 404: response_404})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get(self.password_param)
            converted_uid = serializer.data.get(self.uid_param)
            uid = unconvert_uid(converted_uid)
            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()
            return self.json_success_response(message={"Success": "Password is changed!"})
        return self.json_failed_response(errors=serializer.errors)
