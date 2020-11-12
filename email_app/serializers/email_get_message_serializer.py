from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from email_app.serializers import EmailSerialiser


class EmailGetMessageSerializer(EmailSerialiser):
    message_id = serializers.CharField()
    message_type = serializers.CharField()

    def validate_message_type(self, message_type):
        if message_type != 'raw' and message_type != 'full':
            raise ValidationError("Type of message must be either raw or full")
        return message_type
