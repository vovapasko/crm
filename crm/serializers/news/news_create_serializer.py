from rest_framework import serializers

from .news_serializer import NewsSerializer
from crm.serializers.news.news_attachment_serializer import NewsAttachmentSerializer
from ...models import NewsAttachment


class NewsCreateSerializer(NewsSerializer):
    attachments = serializers.ListField(
        child=NewsAttachmentSerializer(), required=False
    )

    def create(self, validated_data):
        try:
            files = validated_data.pop('attachments')
            attachments = []
            for file in files:
                attachments.append(NewsAttachment(**file))
            validated_data['attachments'] = attachments
        except Exception:
            print("no attachments")
        finally:
            return super().create(validated_data)
