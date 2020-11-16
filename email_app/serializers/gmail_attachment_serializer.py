from .email_serializer import EmailSerialiser
from rest_framework import serializers


class GmailAttachmentSerializer(EmailSerialiser):
    message_id = serializers.CharField()
    attachment_id = serializers.CharField()
