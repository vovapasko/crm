from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ....models import WaveFormationAttachment, WaveFormation


class WaveFormationAttachmentPutSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(use_url=True)
    )
    wave_formation_id = serializers.IntegerField()

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
        wave_formation = WaveFormation.objects.get(pk=self.data.get('wave_formation_id'))
        files = validated_data.pop('file')
        attachments = []
        for file in files:
            attachments.append(WaveFormationAttachment(file=file, wave_formation=wave_formation,
                                                       **validated_data))
        return WaveFormationAttachment.objects.bulk_create(attachments)
