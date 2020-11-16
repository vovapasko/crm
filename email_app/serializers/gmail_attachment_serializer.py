from rest_framework import serializers


class GmailAttachmentSerializer(serializers.Serializer):
    name = serializers.CharField()
    base_64 = serializers.CharField()
    type = serializers.CharField()
