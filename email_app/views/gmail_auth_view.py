from rest_framework.request import Request
from rest_framework.response import Response

from crm.views.base_view import BaseView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class GmailAuthView(BaseView, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_url_key = 'authentication_url'
    state_key = 'state'

    def get(self, request, *args, **kwargs):
        """Sends to client authentication url and state

                Args:
                    kwargs: Additional arguments passed through get request

                Returns:
                    Response[authorization_url: str, state: str]: The generated
                    authorization URL and state. The user must visit the URL to
                    complete the flow. The state is used when completing the flow
                    to verify that the request originated from your application.
                """
        mock_auth_url = 'test url'
        mock_state = 'test state'

        return Response(data={
            self.authentication_url_key: mock_auth_url,
            self.state_key: mock_state
        })

    def post(self, request: Request, *args, **kwargs) -> Response:
        auth_response = request.data['auth_response']
        state = request.data['state']
        return self.make_response(data={
            self.authentication_url_key: auth_response,
            self.state_key: state,
            'success': True
        })
