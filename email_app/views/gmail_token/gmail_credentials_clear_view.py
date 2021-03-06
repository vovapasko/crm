from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from crm.models import NewsEmail
from email_app.serializers import GmailClearCredentialsSerializer
from email_app.views.gmail_token.gmail_token_base_view import GmailTokenBaseView


class GmailCredentialsClearView(GmailTokenBaseView):
    '''
    Clear token for specified email. Credentials will be reased from database, but Gmail Application
    still has access to user account. New authentication will be required.
    '''
    serializer_class = GmailClearCredentialsSerializer
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
                             status.HTTP_204_NO_CONTENT: success_response,
                             status.HTTP_400_BAD_REQUEST: failed_response,
                             status.HTTP_404_NOT_FOUND: not_found_response
                         })
    def delete(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data.get(self.email_key)
            news_email = NewsEmail.objects.get(email=email)
            news_email.gmail_credentials.delete()
            return self.make_response(data=None, status=status.HTTP_204_NO_CONTENT)
        return self.make_response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
