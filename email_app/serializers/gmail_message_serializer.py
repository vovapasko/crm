from rest_framework import serializers
from email_app.serializers.email_serializer import EmailSerialiser
from crm.serializers.news.news_wave_attachment_serializer import NewsWaveAttachmentSerializer


class GmailMessageSerializer(EmailSerialiser):
    email_to = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()
    cc = serializers.CharField(required=False)
    attachments = serializers.ListField(
        child=NewsWaveAttachmentSerializer(), required=False
    )
