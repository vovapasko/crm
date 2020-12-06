from rest_framework import status

from crm.library.helpers.views import format_link, generate_secret, send_dmc_email
from crm.views.base_view import BaseView
from crm.serializers.security import EmailRegisteredSerializer
from crm.library.constants.codes import FORGOT_PASSWORD_LINK_FAILED_STATUS_CODE, \
    FORGOT_PASSWORD_LINK_SUCCESS_STATUS_CODE
from crm.library.constants.views import FORGOT_PASSWORD_LINK, FORGOT_PASSWORD_EMAIL_TEMPLATE


class ForgotPasswordView(BaseView):
    serializer_class = EmailRegisteredSerializer
    template_name = FORGOT_PASSWORD_EMAIL_TEMPLATE
    email_param = 'email'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            response = self.__send_link(email)
            return self.json_success_response(message=response)
        return self.json_failed_response(response_code=status.HTTP_404_NOT_FOUND, errors=serializer.errors)

    def __send_link(self, email: str) -> dict:
        secret_token = generate_secret()
        link = format_link(FORGOT_PASSWORD_LINK)
        try:
            send_dmc_email(
                template=self.template_name,
                receivers=[email],
                subject='Reset password form',
                link=f'{link}/{secret_token}'
                # link format <Host>/<path to password change page>/<data with alert>
            )
            return {FORGOT_PASSWORD_LINK_SUCCESS_STATUS_CODE: email}
        except Exception as e:
            return {FORGOT_PASSWORD_LINK_FAILED_STATUS_CODE: str(e)}
