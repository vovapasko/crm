from rest_framework import serializers

from .attachments import Base64AttachmentSerializer
from .wave_formation_serializer import WaveFormationSerializer
from ...models import WaveFormationAttachment


class WaveFormationCreateSerializer(WaveFormationSerializer):
    attachments = serializers.ListField(
        child=Base64AttachmentSerializer()
    )

    def to_representation(self, instance):
        return super().to_representation(instance)

    def get_attachments(self, instance: WaveFormationAttachment) -> str:
        from .. import WaveFormationAttachmentSerializer

        return WaveFormationAttachmentSerializer(instance.waveformationattachment_set.all(), many=True).data

    def create(self, validated_data: dict) -> WaveFormationAttachment:
        files = validated_data.pop('attachments')
        attachments = []
        for file in files:
            attachments.append(WaveFormationAttachment(file=file))
        # WaveFormationAttachment.objects.bulk_create(attachments)
        validated_data['attachments'] = attachments
        return super().create(validated_data)
