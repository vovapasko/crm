from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from crm.models import NewsEmail
from crm.views.base_view import BaseView
from email_app.serializers.gmail_message_with_ids_serializer import GmailMessageWithIdsSerializer
from email_app.library.gmai_api_view_utils import remove_gmail_message


class EmailRemoveMessagesView(BaseView):
    serializer = GmailMessageWithIdsSerializer

    email_param = 'email'
    message_id_param = 'message_ids'

    email_swagger_param = openapi.Parameter(email_param,
                                            openapi.IN_QUERY,
                                            description='Email for message to permanently remove',
                                            type=openapi.TYPE_STRING)
    message_id_swagger_param = openapi.Parameter(message_id_param,
                                                 openapi.IN_QUERY,
                                                 type=openapi.TYPE_ARRAY,
                                                 items=openapi.Items(type=openapi.TYPE_STRING),
                                                 description='Ids of message to remove')
    swagger_200_response = openapi.Response('[{message_id: Message removed}]')
    swagger_400_response = openapi.Response('{errors: errors here}')

    @swagger_auto_schema(
        manual_parameters=[email_swagger_param, message_id_swagger_param],
        responses={200: swagger_200_response, 400: swagger_400_response}
    )
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
