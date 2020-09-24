from rest_framework.request import Request
from rest_framework.response import Response

from crm.views.base_view import BaseView


class GmailTokenRevokeView(BaseView):
    '''
    Revoke token for specified email. Gmail Application now doesn't have access to user account
    and new authentication will be required.
    '''

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.make_response(data={"Message": "Tokens are revoked"})
