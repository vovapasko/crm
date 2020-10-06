from .email_serializer import EmailSerialiser
from rest_framework import serializers


class InboxEmailSerializer(EmailSerialiser):
    pagination = serializers.IntegerField()
    nextPageToken = serializers.CharField(required=False)

    def validate_pagination(self, pagination: int):
        if pagination <= 0:
            raise ValueError('Pagination must be greater than 0')
        return pagination
