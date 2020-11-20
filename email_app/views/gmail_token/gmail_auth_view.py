from rest_framework import status
from email_app.library.helpers import base64_decode, base64_encode
from email_app.models.credentials import Credentials
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from email_app.views.gmail_token.gmail_token_base_view import GmailTokenBaseView
from email_app.library.gmai_api_view_utils import start_authorize, finish_authorize
from email_app.serializers import GmailCredentialsSerializer
from django.http.response import HttpResponse


class GmailAuthView(GmailTokenBaseView):
    authentication_url_key = 'authentication_url'
    state_key = 'state'

    serializer_class = GmailCredentialsSerializer

    authentication_url_parameter = openapi.Parameter(authentication_url_key,
                                                     openapi.IN_QUERY,
                                                     description="Authentication url for gmail",
                                                     type=openapi.TYPE_STRING)
    state_parameter = openapi.Parameter(state_key, openapi.IN_QUERY,
                                        description="State value for gmail",
                                        type=openapi.TYPE_STRING)

    post_response = openapi.Response('Provides last step for gmail authentication. Provides credentials '
                                     'for user to interact with gmail according to state and authentication url, which '
                                     'are received from client')

    def get(self, request, *args, **kwargs):
        '''This is for google auth redirect. Returns just 200 code if authentication was successful.'''
        # todo Make finish_authorize as async task
        authorization_response = request.build_absolute_uri()
        try:
            state = request.GET['state']
            creds = finish_authorize(
                state=state,
                request_url=authorization_response
            )
            # we make base64_decode on state, because email is encoded in base64 and sent as a state
            Credentials.objects.create_credentials(email=base64_decode(state), **creds)

            return HttpResponse("<p>You are successfully logged in. You can "
                                "close this window now and go back to application</p>")
        except Exception as e:
            print('------------------------------')
            print(e)
            raise e

    @swagger_auto_schema(manual_parameters=[authentication_url_parameter, state_parameter],
                         responses={200: post_response})
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Sends to client authentication url and state

                Args:
                    kwargs: Additional arguments passed through get request

                Returns:
                    Response[authorization_url: str, state: str]: The generated
                    authorization URL and state. The user must visit the URL to
                    complete the flow. The state is used when completing the flow
                    to verify that the request originated from your application.
                """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            auth_url, state = start_authorize(
                par_state=base64_encode(
                    serializer.data.get(self.email_key)
                )
            )
            return Response(data={
                self.authentication_url_key: auth_url,
                self.state_key: state
            })
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
