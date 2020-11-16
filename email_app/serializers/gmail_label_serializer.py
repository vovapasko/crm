from email_app.serializers.email_serializer import EmailSerialiser
from rest_framework import serializers


class GmailLabelSerializer(EmailSerialiser):
    labels = serializers.ListField(child=serializers.CharField())
