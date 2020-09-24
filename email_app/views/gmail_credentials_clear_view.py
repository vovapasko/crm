from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.serializers import Serializer

from crm.views.base_view import BaseView
from rest_framework.request import Request
from rest_framework.response import Response


class GmailCredentialsClearView(BaseView):
    '''
    Clear token for specified email. Credentials will be reased from database, but Gmail Application
    still has access to user account. New authentication will be required.
    '''
    email_key = 'email'

    # for swagger
    email_parameter = openapi.Parameter(email_key, openapi.IN_QUERY,
                                        description="Email credentials of which have to be deleted",
                                        type=openapi.TYPE_STRING)
    success_response = openapi.Response('Credentials were cleared successfully')
    failed_response = openapi.Response('Ty pidor')
    not_found_response = openapi.Response('Requested email does not exist')

    @swagger_auto_schema(manual_parameters=[email_parameter],
                         responses={
                             status.HTTP_200_OK: success_response,
                             status.HTTP_400_BAD_REQUEST: failed_response,
                             status.HTTP_404_NOT_FOUND: not_found_response
                         })
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.make_response(data={"Message": "Credentials cleared"})
