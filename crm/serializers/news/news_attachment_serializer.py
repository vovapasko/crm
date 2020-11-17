from rest_framework import serializers
from crm.models import NewsAttachment, News

# todo remove this serializer and replace with one NewsWaveAttachmentSerializer
class NewsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        exclude = ('news',)
        readonly = ['date_created', 'date_updated']
