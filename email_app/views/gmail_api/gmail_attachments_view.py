from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_attachment_serializer import GmailAttachmentSerializer
from email_app.library.gmail_utils import get_gmail_attachment


class GmailAttachmentsView(BaseView):
    serializer = GmailAttachmentSerializer

    email_param = 'email'
    message_param = 'message_id'
    attachment_param = 'attachment_id'

    def get(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            message_id = serializer.data.get(self.message_param)
            attachment_id = serializer.data.get(self.attachment_param)
            news_email = NewsEmail.objects.get(email=email)
            try:
                attachment = get_gmail_attachment(email=news_email, message_id=message_id,
                                                  attachment_id=attachment_id)
                return self.json_success_response(**attachment)
            except Exception as e:
                return self.json_failed_response(errors={"Exception": str(e)})
        return self.json_failed_response(errors=serializer.errors)
