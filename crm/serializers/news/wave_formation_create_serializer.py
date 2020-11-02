from rest_framework import serializers

from .wave_formation_serializer import WaveFormationSerializer
from crm.serializers.news.wave_formation_attachment_serializer import WaveFormationAttachmentSerializer
from ...models import WaveFormationAttachment


class WaveFormationCreateSerializer(WaveFormationSerializer):
    attachments = serializers.ListField(
        child=WaveFormationAttachmentSerializer()
    )

    def create(self, validated_data: dict) -> WaveFormationAttachment:
        files = validated_data.pop('attachments')
        attachments = []
        for file in files:
            attachments.append(WaveFormationAttachment(**file))
        # WaveFormationAttachment.objects.bulk_create(attachments)
        validated_data['attachments'] = attachments
        return super().create(validated_data)
