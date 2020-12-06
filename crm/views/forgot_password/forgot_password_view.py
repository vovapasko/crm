from crm.views.base_view import BaseView
from crm.serializers.security import EmailRegisteredSerializer
from crm.library.constants.codes import FORGOT_PASSWORD_LINK_FAILED, FORGOT_PASSWORD_LINK_SUCCESS


class ForgotPasswordView(BaseView):
    serializer_class = EmailRegisteredSerializer

    email_param = 'email'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            self.__send_link(email)
            return self.json_success_response(message={
                FORGOT_PASSWORD_LINK_SUCCESS: email})

        return self.json_failed_response(errors=serializer.errors)

    def __send_link(self, email: str) -> None:
        return email
