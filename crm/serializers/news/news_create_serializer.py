from rest_framework import serializers
from .news_serializer import NewsSerializer
from .news_attachment_put_serializer import NewsAttachmentPutSerializer
from ...models import NewsAttachment


class NewsCreateSerializer(NewsSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(use_url=True)
    )

    def validate(self, data):
        print()
        return data

    def create(self, validated_data):
        files = validated_data.pop('attachments')
        attachments = []
        for file in files:
            attachments.append(NewsAttachment(file=file, **validated_data))
        return NewsAttachment.objects.bulk_create(attachments)
