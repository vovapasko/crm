from rest_framework import serializers
from crm.models import WaveFormationAttachment, WaveFormation


class WaveFormationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaveFormationAttachment
        exclude = ('wave_formation',)
        readonly = ['date_created', 'date_updated']
