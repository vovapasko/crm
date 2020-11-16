from typing import Union
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_message_serializer import GmailMessageSerializer
from email_app.library.gmai_api_view_utils import send_gmail_message


class EmailSendMessageView(BaseView):
    serializer_class = GmailMessageSerializer

    email_from_param = 'email'
    email_to_param = 'email_to'
    subject_param = 'subject'
    text_param = 'text'
    cc_param = 'cc'
    attachments_param = 'attachments'

    swagger_cc_param = openapi.Parameter(cc_param, openapi.IN_QUERY,
                                         description="Send copy email to. This is in body parameter!",
                                         type=openapi.TYPE_STRING)
    swagger_email_from_param = openapi.Parameter(email_from_param, openapi.IN_QUERY,
                                                 description="Email from send. This is in body parameter!",
                                                 type=openapi.TYPE_STRING)
    swagger_email_to_param = openapi.Parameter(email_to_param, openapi.IN_QUERY,
                                               description="Email to send. This is in body parameter!",
                                               type=openapi.TYPE_STRING)
    swagger_subject_param = openapi.Parameter(subject_param, openapi.IN_QUERY,
                                              description="Subject of message. This is in body parameter!",
                                              type=openapi.TYPE_STRING)
    swagger_text_param = openapi.Parameter(text_param, openapi.IN_QUERY,
                                           description="Text of message. This is in body parameter!",
                                           type=openapi.TYPE_STRING)
    swagger_attachments_param = openapi.Parameter(attachments_param, openapi.IN_QUERY,
                                                  description="Array of attachments in format "
                                                              "[{type: '', name: '', base_64: ''}, ...]"
                                                              "This is in body parameter!",
                                                  type=openapi.TYPE_STRING, required=False)
    response = openapi.Response('Returns id of message or Exception in format {"Exception": "text"}')

    @swagger_auto_schema(manual_parameters=[swagger_email_from_param,
                                            swagger_email_to_param,
                                            swagger_cc_param,
                                            swagger_subject_param,
                                            swagger_text_param,
                                            swagger_attachments_param],
                         responses={200: response})
    def post(self, request, *args, **kwargs):
        print()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_from = serializer.data.get(self.email_from_param)
            email_to = serializer.data.get(self.email_to_param)
            subject = serializer.data.get(self.subject_param)
            text = serializer.data.get(self.text_param)
            cc = serializer.data.get(self.cc_param, None)
            attachments = serializer.data.get(self.attachments_param, None)
            news_email = NewsEmail.objects.get(email=email_from)
            return self.__send_message(news_email=news_email, email_to=email_to,
                                       subject=subject, text=text,
                                       attachments=attachments,
                                       cc=cc)
        return self.json_failed_response(errors=serializer.errors)

    def __send_message(self, news_email: NewsEmail, email_to: str,
                       subject: str, text: str, attachments: Union[list, None] = None, cc: str = None):
        try:
            message = send_gmail_message(email=news_email, email_to=email_to,
                                         subject=subject, message_text=text,
                                         attachments=attachments, cc=cc)
            return self.json_success_response(message=message)
        except Exception as e:
            return self.json_failed_response(errors={"Exception": str(e)})
