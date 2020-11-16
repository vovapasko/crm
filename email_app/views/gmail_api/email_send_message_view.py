from typing import Union

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
    attachments_param = 'attachments'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_from = serializer.data.get(self.email_from_param)
            email_to = serializer.data.get(self.email_to_param)
            subject = serializer.data.get(self.subject_param)
            text = serializer.data.get(self.text_param)
            attachments = serializer.data.get(self.attachments_param, None)
            news_email = NewsEmail.objects.get(email=email_from)
            return self.__send_message(news_email=news_email, email_to=email_to,
                                       subject=subject, text=text,
                                       attachments=attachments)
        return self.json_failed_response(errors=serializer.errors)

    def __send_message(self, news_email: NewsEmail, email_to: str,
                       subject: str, text: str, attachments: Union[list, None]):
        try:
            message = send_gmail_message(email=news_email, email_to=email_to,
                                         subject=subject, message_text=text,
                                         attachments=attachments)
            return self.json_success_response(message=message)
        except Exception as e:
            return self.json_failed_response(errors={"Exception": str(e)})
