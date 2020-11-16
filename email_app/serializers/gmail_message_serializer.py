from rest_framework import serializers
from email_app.serializers.email_serializer import EmailSerialiser
from email_app.serializers.gmail_attachment_serializer import GmailAttachmentSerializer


class GmailMessageSerializer(EmailSerialiser):
    email_to = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()
    cc = serializers.CharField(required=False)
    attachments = serializers.ListField(
        child=GmailAttachmentSerializer(), required=False
    )
