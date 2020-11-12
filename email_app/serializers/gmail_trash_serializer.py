from email_app.serializers.email_serializer import EmailSerialiser
from rest_framework import serializers


class GmailTrashSerializer(EmailSerialiser):
    max_message_id_len = 200
    message_ids = serializers.ListField(
        child=serializers.CharField(max_length=max_message_id_len)
    )
