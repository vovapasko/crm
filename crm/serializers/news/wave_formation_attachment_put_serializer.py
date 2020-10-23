from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from crm.models import WaveFormationAttachment, WaveFormation
from crm.serializers.news.attachments.base64_attachment_serializer import Base64AttachmentSerializer


class WaveFormationAttachmentPutSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=Base64AttachmentSerializer()
    )

    class Meta:
        model = WaveFormationAttachment
        exclude = ('wave_formation',)
        readonly = ['date_created', 'date_updated']

    def validate_wave_formation_id(self, wave_formation_id: int) -> int:
        try:
            get_object_or_404(WaveFormation, pk=wave_formation_id)
        except Http404:
            raise ValidationError(f"Wave formation with {wave_formation_id} does not exist")
        return wave_formation_id

    def create(self, validated_data: dict) -> WaveFormationAttachment:
        files = validated_data.pop('attachments')
        attachments = []
        for file in files:
            attachments.append(WaveFormationAttachment(file=file,
                                                       **validated_data))
        return WaveFormationAttachment.objects.bulk_create(attachments)
