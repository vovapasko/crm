from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from crm.library.helpers.views import format_link, send_dmc_email, convert_uid
from crm.models import User
from crm.views.base_view import BaseView
from crm.serializers.security import EmailRegisteredSerializer
from crm.library.constants.codes import FORGOT_PASSWORD_LINK_FAILED_STATUS_CODE, \
    FORGOT_PASSWORD_LINK_SUCCESS_STATUS_CODE
from crm.library.constants.views import FORGOT_PASSWORD_LINK, FORGOT_PASSWORD_EMAIL_TEMPLATE
from django.contrib.auth.tokens import default_token_generator


class ForgotPasswordView(BaseView):
    serializer_class = EmailRegisteredSerializer
    template_name = FORGOT_PASSWORD_EMAIL_TEMPLATE
    email_param = 'email'

    email_swagger_param = openapi.Parameter(name=email_param, in_=openapi.IN_QUERY,
                                            description="Email for which you need to reset password",
                                            required=True, type=openapi.TYPE_STRING)

    response_404 = openapi.Response(
        description="404 Error in dict {errors: Error type}. No such a user with this email"
    )
    response_200 = openapi.Response(
        description="If message was sent to email without errors, you will get dict"
                    "{FORGOT_PASSWORD_LINK_SUCCESS: email for which was success sending}. "
                    "If message was sent to email with error, you will get dict "
                    "{FORGOT_PASSWORD_LINK_FAILED: exception in str}"
    )

    @swagger_auto_schema(manual_parameters=[email_swagger_param],
                         responses={200: response_200, 404: response_404})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            response = self.__send_link(email)
            return self.json_success_response(message=response)
        return self.json_failed_response(response_code=status.HTTP_404_NOT_FOUND, errors=serializer.errors)

    def __send_link(self, email: str) -> dict:
        user = User.objects.get(email=email)
        secret_token = default_token_generator.make_token(
            user=user
        )
        uid = convert_uid(user.id)
        link = format_link(FORGOT_PASSWORD_LINK)
        try:
            send_dmc_email(
                template=self.template_name,
                receivers=[email],
                subject='Reset password form',
                link=f'{link}/{uid}/{secret_token}'
                # link format <Host>/<path to password change page>/<data with alert>
            )
            return {FORGOT_PASSWORD_LINK_SUCCESS_STATUS_CODE: email}
        except Exception as e:
            return {FORGOT_PASSWORD_LINK_FAILED_STATUS_CODE: str(e)}
