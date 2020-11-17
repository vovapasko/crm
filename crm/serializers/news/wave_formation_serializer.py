from rest_framework import serializers

from .news_email_serializer import NewsEmailSerializer
from crm.models import WaveFormation, NewsWaveAttachment
from drf_writable_nested import WritableNestedModelSerializer
from crm.serializers.news.news_wave_attachment_serializer import NewsWaveAttachmentSerializer


class WaveFormationSerializer(WritableNestedModelSerializer):
    email = NewsEmailSerializer()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = WaveFormation
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
        depth = 1

    def get_attachments(self, instance: NewsWaveAttachment) -> str:
        return NewsWaveAttachmentSerializer(instance.waveformationattachment_set.all(), many=True).data

    def create(self, validated_data):
        return super().create(validated_data)
