from rest_framework import serializers

from .wave_formation_attachment_serializer import WaveFormationAttachmentSerializer
from .news_email_serializer import NewsEmailSerializer
from crm.models import WaveFormation, WaveFormationAttachment
from drf_writable_nested import WritableNestedModelSerializer


# todo remove this serializer and replace with one NewsWaveAttachmentSerializer
class WaveFormationSerializer(WritableNestedModelSerializer):
    email = NewsEmailSerializer()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = WaveFormation
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
        depth = 1

    def get_attachments(self, instance: WaveFormationAttachment) -> str:
        return WaveFormationAttachmentSerializer(instance.waveformationattachment_set.all(), many=True).data

    def create(self, validated_data):
        return super().create(validated_data)
