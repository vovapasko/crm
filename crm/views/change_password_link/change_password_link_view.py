from django.core import signing
from rest_framework.permissions import IsAuthenticated
from ..base_view import BaseView
from ...library.constants import *
from ...library.helpers import send_dmc_email
from rest_framework.response import Response
from rest_framework.request import Request

from ...library.helpers.views import format_link


class ChangePasswordLinkView(BaseView):
    """
    View for generating change password link
    """
    permission_classes = (IsAuthenticated,)
    template_name = PASSWORD_CHANGE_EMAIL

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        :return: json response
            http response codes:
                200 - ok, email was sent
            keys:
                success - true email sent, false otherwise
        """
        return self.__generate_and_send_link(request)

    def __generate_and_send_link(self, request: Request) -> Response:
        try:
            self.__send_email(request)
        except:
            return self.json_failed_response(
                errors=dict(message="Can not send email")
            )
        return self.json_success_response()

    def __send_email(self, request: Request) -> Response:
        """
        sends confirmation link to user from request email
        """
        data = signing.dumps(dict(id=request.user.id))
        link = format_link(CHANGE_PASSWORD_LINK)
        send_dmc_email(
            self.template_name,
            [request.user.email],
            subject='Password change confirm',
            link=f'{link}/{data}'
            # link format <Host>/<path to password change page>/<data with alert>
        )
