from drf_yasg import openapi
from rest_framework.request import Request
from rest_framework.response import Response
from email_app.views.gmail.gmail_token_base_view import GmailTokenBaseView


class GmailTokenRevokeView(GmailTokenBaseView):
    '''
    Revoke token for specified email. Gmail Application now doesn't have access to user account
    and new authentication will be required.
    '''

    # for swagger
    email_parameter = openapi.Parameter(
        GmailTokenBaseView.email_key, openapi.IN_QUERY,
        description="Email credentials of which have to be deleted. "
                    "It has to be in BODY. It has here in query status, because swagger"
                    " generating library doesn't work correctly ",
        type=openapi.TYPE_STRING,
    )
    success_response = openapi.Response('Credentials were cleared successfully', GmailTokenBaseView.serializer_class)
    failed_response = openapi.Response('Some errors happened', GmailTokenBaseView.serializer_class)
    not_found_response = openapi.Response('Requested email does not exist', GmailTokenBaseView.serializer_class)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.make_response(data={"Message": "Tokens are revoked"})
