from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from crm.models import NewsAttachment, News


class NewsAttachmentPutSerializer(serializers.ModelSerializer):
    """
    Because of incorrect serialization of ListField in file, you should
    use this serializer only in creating attachments. For other purposes use NewsAttachmentSerializer
    """
    file = serializers.ListField(
        child=serializers.FileField(use_url=True)
    )
    news_id = serializers.IntegerField()

    class Meta:
        model = NewsAttachment
        exclude = ('news',)
        readonly = ['date_created', 'date_updated']

    def validate_news_id(self, news_id: int) -> int:
        try:
            get_object_or_404(News, pk=news_id)
        except Http404:
            raise ValidationError(f"News with {news_id} does not exist")
        return news_id

    def create(self, validated_data: dict) -> NewsAttachment:
        news = News.objects.get(pk=self.data.get('news_id'))
        files = validated_data.pop('file')
        attachments = []
        for file in files:
            attachments.append(NewsAttachment(file=file, news=news, **validated_data))
        return NewsAttachment.objects.bulk_create(attachments)