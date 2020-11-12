from rest_framework import serializers

from email_app.serializers import EmailSerialiser


class EmailGetMessageSerializer(EmailSerialiser):
    message_id = serializers.CharField()
