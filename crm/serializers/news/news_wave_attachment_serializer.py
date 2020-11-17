from rest_framework import serializers
from crm.models.burst_news.news_wave_attachment import NewsWaveAttachment


class NewsWaveAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsWaveAttachment
        exclude = ('wave_formation', 'news')
        readonly = ['date_created', 'date_updated']
