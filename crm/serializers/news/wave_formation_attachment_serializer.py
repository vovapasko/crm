from rest_framework import serializers
from crm.models import WaveFormationAttachment, WaveFormation

# todo remove this serializer and replace with one NewsWaveAttachmentSerializer
class WaveFormationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaveFormationAttachment
        exclude = ('wave_formation',)
        readonly = ['date_created', 'date_updated']
