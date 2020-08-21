from rest_framework import serializers
from crm.models.burst_news.news_wave_price_list import NewsWavePriceList


class NewsWavePriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsWavePriceList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1
