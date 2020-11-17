from rest_framework import serializers
from crm.models.burst_news.news_wave_attachment import NewsWaveAttachment
from crm.serializers.news.wave_formation_serializer import WaveFormationSerializer
from crm.serializers.news.news_wave_attachment_serializer import NewsWaveAttachmentSerializer


class WaveFormationCreateSerializer(WaveFormationSerializer):
    attachments = serializers.ListField(
        child=NewsWaveAttachmentSerializer(), required=False
    )

    def create(self, validated_data: dict) -> NewsWaveAttachment:
        try:
            files = validated_data.pop('attachments')
            attachments = []
            for file in files:
                attachments.append(NewsWaveAttachment(**file))
            validated_data['attachments'] = attachments
        except Exception:
            print("no attachments")
        finally:
            return super().create(validated_data)
