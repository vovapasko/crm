from rest_framework import serializers


class GmailAttachmentSerializer(serializers.Serializer):
    name = serializers.CharField()
    base64 = serializers.CharField()
    type = serializers.CharField()
