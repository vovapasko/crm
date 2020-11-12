from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_message_with_ids_serializer import GmailMessageWithIdsSerializer
from email_app.library.gmail_utils import remove_gmail_message


class EmailRemoveMessagesView(BaseView):
    serializer = GmailMessageWithIdsSerializer

    email_param = 'email'
    message_id_param = 'message_ids'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            news_email = NewsEmail.objects.get(email=email)
            message_ids = serializer.data.get(self.message_id_param)
            results = {}
            for message_id in message_ids:
                try:
                    remove_gmail_message(email=news_email, message_id=message_id)
                    results.update({message_id: "Message removed"})
                except Exception as e:
                    results.update({message_id: str(e)})
            return self.json_success_response(**results)
        return self.json_failed_response(errors=serializer.errors)
