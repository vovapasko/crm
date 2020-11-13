from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_label_serializer import GmailLabelSerializer
from email_app.library.gmail_utils import filter_label_gmail_message


class FilterLabelsGmailMessagesView(BaseView):
    serializer = GmailLabelSerializer

    email_param = 'email'
    labels_param = 'labels'

    def get(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            labels = serializer.data.get(self.labels_param)
            news_email = NewsEmail.objects.get(email=email)
            messages = filter_label_gmail_message(email=news_email, labels=labels)
            return self.json_success_response(**messages)
        return self.json_failed_response(errors=serializer.errors)
