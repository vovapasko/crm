from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.library.gmai_api_view_utils import untrash_gmail_message
from email_app.serializers import GmailMessageWithIdsSerializer


class UntrashMessageView(BaseView):
    serializer_class = GmailMessageWithIdsSerializer

    email_param = 'email'
    message_id_param = 'message_ids'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            news_email = NewsEmail.objects.get(email=email)
            message_ids = serializer.data.get(self.message_id_param)
            results = {}
            for message_id in message_ids:
                message = untrash_gmail_message(email=news_email, message_id=message_id)
                results.update({message_id: message})
            return self.json_success_response(**results)
        return self.json_failed_response(errors=serializer.errors)
