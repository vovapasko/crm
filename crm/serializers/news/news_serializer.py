from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .news_attachment_serializer import NewsAttachmentSerializer
from .news_email_serializer import NewsEmailSerializer
from crm.serializers import ContractorSerializer
from crm.models import News, NewsAttachment


class NewsSerializer(WritableNestedModelSerializer):
    contractors = ContractorSerializer(many=True)
    email = NewsEmailSerializer()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
        depth = 1

    def get_attachments(self, instance: NewsAttachment) -> str:
        return NewsAttachmentSerializer(instance.newsattachment_set.all(), many=True).data
