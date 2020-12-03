from rest_framework.permissions import IsAuthenticated

from crm.views.base_view import BaseView
from email_app.serializers import GmailCredentialsSerializer


class GmailTokenBaseView(BaseView):
    serializer_class = GmailCredentialsSerializer
    # todo add here custom permission which forbids access to Guest
    permission_classes = [IsAuthenticated]
    email_key = 'email'
