from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request

from crm.models import NewsEmail
from crm.views.base_view import BaseView
from crm.paginations import SmallResultsSetPagination
from email_app.serializers.inbox_email_serializer import InboxEmailSerializer
from email_app.library.gmai_api_view_utils import get_gmail_messages, get_gmail_labels, get_gmail_profile


class EmailInboxView(BaseView):
    pagination_class = SmallResultsSetPagination
    serializer_class = InboxEmailSerializer

    email_param = 'email'
    pagination_param = 'pagination'
    next_page_token_param = 'nextPageToken'

    email_swagger_parameter = openapi.Parameter(email_param,
                                                openapi.IN_QUERY,
                                                description="Email for inbox",
                                                type=openapi.TYPE_STRING)
    pagination_swagger_parameter = openapi.Parameter(pagination_param, openapi.IN_QUERY,
                                                     description="Amount of messages, which you want to get",
                                                     type=openapi.TYPE_STRING)
    next_page_token_swagger_parameter = openapi.Parameter(next_page_token_param, openapi.IN_QUERY,
                                                          description="Token parameter to get the next messages",
                                                          type=openapi.TYPE_STRING,
                                                          required=False)

    response_swagger = openapi.Response('Gives dictionary of messages, profile and labels for this email')

    @swagger_auto_schema(
        manual_parameters=[email_swagger_parameter, pagination_swagger_parameter, next_page_token_swagger_parameter],
        responses={200: response_swagger})
    def get(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            pagination = serializer.data.get(self.pagination_param)
            next_page_token = serializer.data.get(self.next_page_token_param, None)
            news_email = NewsEmail.objects.get(email=email)
            messages = get_gmail_messages(email=news_email, pagination=pagination, next_page_token=next_page_token)
            labels = get_gmail_labels(email=news_email)
            profile = get_gmail_profile(email=news_email)
            response = {**messages, **labels, **profile}
            return self.make_response(data=response)
        return self.json_failed_response(errors=serializer.errors)
