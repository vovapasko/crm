from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .news_wave_attachment_serializer import NewsWaveAttachmentSerializer
from .news_email_serializer import NewsEmailSerializer
from crm.serializers import ContractorSerializer
from crm.models import News, NewsWaveAttachment


class NewsSerializer(WritableNestedModelSerializer):
    contractors = ContractorSerializer(many=True)
    email = NewsEmailSerializer()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
        depth = 1

    def get_attachments(self, instance: NewsWaveAttachment) -> str:
        return NewsWaveAttachmentSerializer(instance.newsattachment_set.all(), many=True).data
