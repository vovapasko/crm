from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from email_app.serializers import GmailCredentialsSerializer
from email_app.views.gmail.gmail_token_base_view import GmailTokenBaseView


class GmailCredentialsClearView(GmailTokenBaseView):
    '''
    Clear token for specified email. Credentials will be reased from database, but Gmail Application
    still has access to user account. New authentication will be required.
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

    @swagger_auto_schema(manual_parameters=[email_parameter],
                         responses={
                             status.HTTP_200_OK: success_response,
                             status.HTTP_400_BAD_REQUEST: failed_response,
                             status.HTTP_404_NOT_FOUND: not_found_response
                         })
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.make_response(data={"Message": "Credentials cleared"})
