from django.db.models import QuerySet
from rest_framework.request import Request

from crm.models import NewsEmail
from crm.views.base_view import BaseView
from rest_framework.generics import GenericAPIView
from crm.paginations import SmallResultsSetPagination
from email_app.serializers.email_serializer import EmailSerialiser
from email_app.library.gmail_utils import get_gmail_messages, get_gmail_labels


class EmailInboxView(BaseView):
    '''
    Returns labels and first messages of
    '''
    pagination_class = SmallResultsSetPagination
    serializer_class = EmailSerialiser

    email_param = 'email'

    def get(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get('email')
            news_email = NewsEmail.objects.get(email=email)
            messages = get_gmail_messages(email=news_email)
            labels = get_gmail_labels(email=news_email)
            response = {"messages": messages, **labels}
            return self.make_response(data=response)
        return self.json_failed_response(errors=serializer.errors)
