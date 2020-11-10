from rest_framework import serializers
from crm.models import NewsAttachment, News


class NewsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        exclude = ('news',)
        readonly = ['date_created', 'date_updated']
