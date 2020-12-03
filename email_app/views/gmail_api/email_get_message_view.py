from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.email_get_message_serializer import EmailGetMessageSerializer
from email_app.library.gmai_api_view_utils import get_raw_gmail_message, get_full_gmail_message
from googleapiclient.errors import HttpError


class EmailGetMessageView(BaseView):
    serializer_class = EmailGetMessageSerializer

    email_param = 'email'
    message_id_param = 'message_id'
    message_type_param = 'message_type'

    email_swagger_parameter = openapi.Parameter(email_param,
                                                openapi.IN_QUERY,
                                                description="Email for message to get",
                                                type=openapi.TYPE_STRING)
    message_id_swagger_parameter = openapi.Parameter(message_id_param, openapi.IN_QUERY,
                                                     description="ID of messages, which you want to get",
                                                     type=openapi.TYPE_STRING)
    message_type_param_swagger_parameter = openapi.Parameter(message_type_param, openapi.IN_QUERY,
                                                             description="Type parameter of message. Can be row or full",
                                                             type=openapi.TYPE_STRING)

    response_swagger = openapi.Response('Gives message for this email according to the required type')

    @swagger_auto_schema(
        manual_parameters=[email_swagger_parameter, message_id_swagger_parameter,
                           message_type_param_swagger_parameter],
        responses={200: response_swagger})
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            message_id = serializer.data.get(self.message_id_param)
            news_email = NewsEmail.objects.get(email=email)
            message_type = serializer.data.get(self.message_type_param)
            if message_type == 'raw':
                return self.__get_raw_message(news_email=news_email, message_id=message_id)
            else:
                return self.__get_full_message(news_email, message_id=message_id)
        return self.json_failed_response(errors=serializer.errors)

    def __get_raw_message(self, news_email: NewsEmail, message_id: str):
        try:
            message = get_raw_gmail_message(email=news_email, message_id=message_id)
            return self.json_success_response(
                **message
            )
        except HttpError as e:
            return self.json_failed_response(
                errors={'error': str(e.content)}
            )

    def __get_full_message(self, news_email: NewsEmail, message_id: str):
        try:
            message = get_full_gmail_message(email=news_email, message_id=message_id)
            return self.json_success_response(
                **message
            )
        except HttpError as e:
            return self.json_failed_response(
                errors={'error': str(e.content)}
            )
