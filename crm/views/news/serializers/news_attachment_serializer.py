from rest_framework import serializers
from ....models import NewsAttachment, News


class NewsAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    news_id = serializers.IntegerField()

    class Meta:
        model = NewsAttachment
        exclude = ('news',)
        readonly = ['date_created', 'date_updated']
