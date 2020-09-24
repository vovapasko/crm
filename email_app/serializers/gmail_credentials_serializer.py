from rest_framework import serializers


class GmailCredentialsSerializer(serializers.Serializer):
    email_field = serializers.EmailField()
