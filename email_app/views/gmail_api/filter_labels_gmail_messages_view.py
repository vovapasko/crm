from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_label_serializer import GmailLabelSerializer
from email_app.library.gmai_api_view_utils import filter_label_gmail_message
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class FilterLabelsGmailMessagesView(BaseView):
    serializer = GmailLabelSerializer

    email_param = 'email'
    labels_param = 'labels'

    email_swagger_param = openapi.Parameter(email_param,
                                            openapi.IN_QUERY,
                                            description='Email where filtering should be',
                                            type=openapi.TYPE_STRING)
    labes_swagger_param = openapi.Parameter(labels_param,
                                            openapi.IN_QUERY,
                                            type=openapi.TYPE_STRING,
                                            description='Label to filter')
    swagger_200_response = openapi.Response('Messages list')
    swagger_400_response = openapi.Response('{errors: errors here}')

    @swagger_auto_schema(
        manual_parameters=[email_swagger_param, labes_swagger_param],
        responses={200: swagger_200_response, 400: swagger_400_response}
    )
    def get(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.GET)
        if serializer.is_valid():
            email = serializer.data.get(self.email_param)
            labels = serializer.data.get(self.labels_param)
            news_email = NewsEmail.objects.get(email=email)
            messages = filter_label_gmail_message(email=news_email, labels=labels)
            return self.json_success_response(**messages)
        return self.json_failed_response(errors=serializer.errors)
