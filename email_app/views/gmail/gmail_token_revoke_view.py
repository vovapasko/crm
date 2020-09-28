import requests
from drf_yasg import openapi
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from crm.models import NewsEmail
from email_app.models import Credentials
from email_app.views.gmail.gmail_token_base_view import GmailTokenBaseView
from email_app.serializers.gmail_clear_credentials_serializer import GmailClearCredentialsSerializer


class GmailTokenRevokeView(GmailTokenBaseView):
    '''
    Revoke token for specified email. Gmail Application now doesn't have access to user account
    and new authentication will be required.
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

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            credentials = NewsEmail.objects.get(email=serializer.data.get(self.email_key)).gmail_credentials
            revoke = requests.post('https://oauth2.googleapis.com/revoke',
                                   params={'token': credentials.token},
                                   headers={'content-type': 'application/x-www-form-urlencoded'})

            status_code = getattr(revoke, 'status_code')
            if status_code == status.HTTP_200_OK:
                message = 'Credentials successfully revoked'
                credentials.is_revoked = True
                credentials.save()
            else:
                message = f'Error {status_code} occured'
            return self.make_response(data=message, status=status.HTTP_200_OK)
        return self.make_response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
